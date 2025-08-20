
from flask import Blueprint, request, jsonify
from bl.report_service import ReportService
from models.report import Report

report_api = Blueprint("report_api", __name__)
report_service = ReportService()

@report_api.route("/reports", methods=["POST"])
def submit_report():
    report = Report(**request.json)
    report_id = report_service.submit_report(report)
    return jsonify({"id": report_id}), 201

@report_api.route("/reports", methods=["GET"])
def get_all_reports():
    reports = report_service.get_all_reports()
    return jsonify([r.dict() for r in reports])

@report_api.route("/reports/<int:report_id>/resolve", methods=["PUT"])
def resolve_report(report_id):
    data = request.json
    status = data.get("status", "resolved")
    report_service.resolve_report(report_id, status)
    return jsonify({"message": f"Report marked as {status}"})

