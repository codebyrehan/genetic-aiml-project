const $=id=>document.getElementById(id);
const mismatch=$('mismatches'),conservation=$('conservation'),gc=$('gc');
let lastRisk=null,lastEco=null,lastReg=null;
const scenarios={
 baseline:{mismatches:2,pam_correct:true,in_exon:true,conservation_score:.72,gc_content:.48,gene_drive:false,off_target_sites:2,population_impact:.2,uncertainty:.2,ethical_flags:1},
 offtarget:{mismatches:5,pam_correct:false,in_exon:true,conservation_score:.52,gc_content:.55,gene_drive:false,off_target_sites:8,population_impact:.5,uncertainty:.4,ethical_flags:2},
 drive:{mismatches:3,pam_correct:true,in_exon:true,conservation_score:.62,gc_content:.5,gene_drive:true,off_target_sites:5,population_impact:.8,uncertainty:.65,ethical_flags:3},
 conserved:{mismatches:1,pam_correct:true,in_exon:false,conservation_score:.94,gc_content:.46,gene_drive:false,off_target_sites:1,population_impact:.1,uncertainty:.15,ethical_flags:0}
};
function sync(){ $('mismatch-out').value=mismatch.value;$('conservation-out').value=Number(conservation.value).toFixed(2);$('gc-out').value=Number(gc.value).toFixed(2) }
[mismatch,conservation,gc].forEach(x=>x.addEventListener('input',sync));sync();
function pct(v){return `${Math.max(0,Math.min(100,Number(v)||0))}%`}
function setMeter(id,v){const el=$(id);if(el)el.style.width=pct(v)}
function setDashboard(risk,eco,reg){
 const rv=risk?.risk_score||0,ev=eco?.score||0,gv=reg?.regulatory_signal||0;
 $('dash-genetic').textContent=`${rv}%`; $('dash-eco').textContent=`${ev}%`; $('dash-reg').textContent=`${gv}%`;
 setMeter('genetic-meter',rv);setMeter('eco-meter',ev);setMeter('reg-meter',gv);
 const level=rv>=67||ev>=67||gv>=70?'Elevated review signal':rv>=40||ev>=34||gv>=40?'Moderate review signal':'Lower educational signal';
 $('insight-title').textContent=level;
 $('insight-copy').textContent=`Genetic ${rv}% · ecological ${ev}% · governance ${gv}%. These are synthetic decision-support signals, not approvals or clinical predictions.`;
}
async function post(url,payload){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const data=await r.json();if(!r.ok)throw Error(data.error||'Request failed');return data}
async function runProfile(payload,showResult=true){
 const risk=await post('/api/analyze',payload);
 const eco=await post('/api/ecological-risk',{gene_drive:payload.gene_drive??false,off_target_sites:payload.off_target_sites??Math.max(0,payload.mismatches),population_impact:payload.population_impact??.25,uncertainty:payload.uncertainty??.25});
 const reg=await post('/api/regulatory-assessment',{genetic_score:Number(risk.risk_score),ecological_score:Number(eco.score),ethical_flags:payload.ethical_flags??1});
 lastRisk=risk;lastEco=eco;lastReg=reg;setDashboard(risk,eco,reg);
 if(showResult){
  $('score').textContent=risk.risk_score+'%';$('risk-label').textContent=risk.label;$('risk-copy').textContent=`${risk.model} evaluated this synthetic profile with ${risk.confidence}% confidence. Educational signal only.`;$('result-state').textContent='ANALYSIS COMPLETE';
  $('impact-mismatch').textContent=risk.feature_importance.mismatches>.2?'HIGH':'LOW';$('impact-pam').textContent=risk.feature_importance.pam_correct>.1?'HIGH':'LOW';$('impact-exon').textContent=risk.feature_importance.in_exon>.1?'MEDIUM':'LOW';$('impact-conservation').textContent=risk.feature_importance.conservation_score>.1?'MEDIUM':'LOW';
  const ring=Math.max(1,Math.min(99,Number(risk.risk_score)||1));$('score-ring').style.background=`radial-gradient(circle at center,var(--panel) 58%,transparent 59%),conic-gradient(var(--cyan) 0 ${ring}%,#18313b ${ring}% 100%)`;$('report-btn').disabled=false;
 }
 return {risk,eco,reg}
}
$('risk-form').addEventListener('submit',async e=>{e.preventDefault();const payload={mismatches:+mismatch.value,pam_correct:$('pam').checked,in_exon:$('exon').checked,conservation_score:+conservation.value,gc_content:+gc.value,gene_drive:false,off_target_sites:+mismatch.value,population_impact:.25,uncertainty:.25,ethical_flags:1};$('result-state').textContent='ANALYZING…';$('risk-label').textContent='Running intelligence pipeline';try{await runProfile(payload)}catch(err){$('result-state').textContent='ERROR';$('risk-label').textContent='Analysis unavailable';$('risk-copy').textContent=err.message}});
$('report-btn').addEventListener('click',async()=>{if(!lastRisk)return;const r=await fetch('/api/report',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({risk:lastRisk,ecological:lastEco,regulatory:lastReg})});if(!r.ok){alert('Report generation failed.');return}const blob=await r.blob();const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='genova-assessment.pdf';a.click();URL.revokeObjectURL(url)});
async function runScenario(name){const s=scenarios[name];$('scenario-score').textContent='…';$('scenario-copy').textContent='Running three-engine comparison';try{const out=await runProfile(s,false);const avg=(Number(out.risk.risk_score)*.45)+(Number(out.eco.score)*.3)+(Number(out.reg.regulatory_signal)*.25);$('scenario-score').textContent=Math.round(avg)+'%';$('scenario-copy').textContent=`${out.risk.label} genetic signal · ${out.eco.label} ecological signal · ${out.reg.level} governance pressure.`;setMeter('sim-genetic',out.risk.risk_score);setMeter('sim-eco',out.eco.score);setMeter('sim-reg',out.reg.regulatory_signal);$('sim-genetic-text').textContent=out.risk.risk_score+'%';$('sim-eco-text').textContent=out.eco.score+'%';$('sim-reg-text').textContent=out.reg.regulatory_signal+'%'}catch(err){$('scenario-copy').textContent=err.message}}
document.querySelectorAll('.scenario').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.scenario').forEach(x=>x.classList.remove('active'));btn.classList.add('active');runScenario(btn.dataset.scenario)}));
$('patterns-btn').addEventListener('click',async()=>{const b=$('patterns-btn');b.textContent='Refreshing…';try{const d=await fetch('/api/patterns').then(r=>r.json());b.textContent=`Pattern Summary Ready · ${d.k??3} clusters`}catch(e){b.textContent='Pattern service unavailable'}});
runScenario('baseline');
