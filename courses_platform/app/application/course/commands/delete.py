from app.request_objects import Request
from app.response_objects import Response, ResponseFailure, ResponseSuccess

from app.persistence.database.course import course_model as cm
from app.application.interfaces.idb_session import DbSession
from app.application.course.exceptions import NoMatchingCourse
from app.application.interfaces.icommand_query import ICommandQuery


class DeleteCourseCommand(ICommandQuery):
    def __init__(self, db_session: DbSession) -> None:
        self.db_session = db_session

    def execute(self, request: Request) -> Response:
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            with self.db_session() as db:
                result = db.query(cm.Course).\
                            filter(cm.Course.id == request.course_id).\
                            delete()

            if not result:
                return ResponseFailure.build_resource_error(
                    NoMatchingCourse(
                        f'No Course has been found for a given id: {request.course_id}')
                )

            return ResponseSuccess.build_response_no_content()

        except Exception as exc:
            return ResponseFailure.build_system_error(exc)
