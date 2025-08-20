
from dal.repository.report_repository import ReportRepository
from models.report import Report

class ReportService:
    def __init__(self):
        self.repo = ReportRepository()

    def submit_report(self, report: Report) -> int:
        return self.repo.add(report)

    def get_all_reports(self) -> list[Report]:
        return self.repo.get_all()

    def resolve_report(self, report_id: int, status: str):
        self.repo.update_status(report_id, status)
