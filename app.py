import sys
sys.path.insert(0,'.')
from flask import Flask,request,jsonify
from src.analytics import AnalyticsService,AnalyticsError
s=AnalyticsService();app=Flask(__name__)
def out(d):return jsonify(id=d.id,supplierId=d.supplier_id,state=d.state,inputHash=d.input_hash,defectRate=d.defect_rate,onTimeRate=d.on_time_rate,artifactPath=d.artifact_path,expiresOn=d.expires_on)
@app.errorhandler(AnalyticsError)
def er(e):return jsonify(error=e.message),{'validation':400,'forbidden':403,'not_found':404}.get(e.kind,409)
@app.post('/reports')
def create():return out(s.create(request.headers.get('X-Role',''),request.headers.get('X-Actor',''),request.args.get('id',''),request.args.get('supplierId',''),float(request.args.get('defects','-1')),float(request.args.get('deliveries','-1')),float(request.args.get('late','-1'))))
@app.post('/reports/chart')
def chart():return out(s.chart(request.headers.get('X-Role',''),request.headers.get('X-Actor',''),request.args.get('id','')))
@app.post('/reports/review')
def review():return out(s.review(request.headers.get('X-Role',''),request.headers.get('X-Actor',''),request.args.get('id',''),request.args.get('notes','')))
@app.post('/reports/publish')
def publish():return out(s.decide(request.headers.get('X-Role',''),request.headers.get('X-Actor',''),request.args.get('id',''),True,request.args.get('reason',''),request.args.get('expiresOn','')))
@app.post('/reports/reject')
def reject():return out(s.decide(request.headers.get('X-Role',''),request.headers.get('X-Actor',''),request.args.get('id',''),False,request.args.get('reason','')))
@app.post('/reports/revoke')
def revoke():return out(s.revoke(request.headers.get('X-Role',''),request.headers.get('X-Actor',''),request.args.get('id',''),request.args.get('reason','')))
if __name__=='__main__':app.run(host='0.0.0.0',port=17500)

