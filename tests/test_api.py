import io

import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_analyze_endpoint(client):
    response = client.post('/api/analyze', json={'mismatches': 2, 'pam_correct': True, 'in_exon': True, 'conservation_score': 0.72, 'gc_content': 0.48})
    assert response.status_code == 200
    assert 0 <= response.get_json()['risk_score'] <= 100


def test_analyze_validates_required_fields(client):
    response = client.post('/api/analyze', json={'mismatches': 1})
    assert response.status_code == 400
    assert 'Missing fields' in response.get_json()['error']


def test_patterns_endpoint(client):
    assert client.get('/api/patterns').status_code == 200


def test_ecological_endpoint(client):
    response = client.post('/api/ecological-risk', json={'gene_drive': True, 'off_target_sites': 2, 'population_impact': 0.5, 'uncertainty': 0.2})
    assert response.status_code == 200
    assert 'score' in response.get_json()


def test_regulatory_endpoint(client):
    response = client.post('/api/regulatory-assessment', json={'genetic_score': 90, 'ecological_score': 80, 'ethical_flags': 4})
    assert response.status_code == 200
    data = response.get_json()
    assert data['level'] == 'HIGH'
    assert 'human review' in data['recommendation'].lower()


def test_ecological_validation(client):
    response = client.post('/api/ecological-risk', json={'gene_drive': True, 'off_target_sites': -1, 'population_impact': 0.5, 'uncertainty': 0.2})
    assert response.status_code == 400


def test_regulatory_validation(client):
    response = client.post('/api/regulatory-assessment', json={'genetic_score': 101, 'ecological_score': 50, 'ethical_flags': 0})
    assert response.status_code == 400


def test_model_metrics(client):
    response = client.get('/api/model-metrics')
    assert response.status_code == 200
    data = response.get_json()
    assert set(data['metrics']) == {'accuracy', 'precision', 'recall', 'f1'}
    assert len(data['confusion_matrix']) == 2
    assert data['dataset_size'] == 8000


def test_dataset_profile(client):
    csv = b'mismatches,pam_correct,in_exon,conservation_score,gc_content\n2,true,true,0.72,0.48\n4,false,true,0.41,0.55\n'
    response = client.post('/api/dataset-profile', data={'file': (io.BytesIO(csv), 'sample.csv')}, content_type='multipart/form-data')
    assert response.status_code == 200
    data = response.get_json()
    assert data['rows'] == 2
    assert 'mismatches' in data['supported_features']


def test_dataset_profile_rejects_non_csv(client):
    response = client.post('/api/dataset-profile', data={'file': (io.BytesIO(b'hello'), 'sample.txt')}, content_type='multipart/form-data')
    assert response.status_code == 400


def test_report_requires_analysis(client):
    response = client.post('/api/report', json={})
    assert response.status_code == 400


def test_report_generation(client):
    response = client.post('/api/report', json={'risk': {'risk_score': 42.0, 'label': 'MODERATE', 'model': 'Random Forest', 'confidence': 88.0}, 'ecological': {'score': 30.0, 'label': 'LOW'}, 'regulatory': {'regulatory_signal': 35.0, 'level': 'LOW', 'recommendation': 'Review'}})
    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'
    assert response.data.startswith(b'%PDF')
