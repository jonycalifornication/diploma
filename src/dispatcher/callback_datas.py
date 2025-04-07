from aiogram.filters.callback_data import CallbackData


class CourseCallback(CallbackData, prefix="course"):
    course_id: str


class EnrollmentCallback(CallbackData, prefix="enrollment"):
    course_enroll: bool
    course_id: str


class CourseQuestionCallback(CallbackData, prefix="question"):
    course_id: str

class InstructorCallback(CallbackData, prefix="instructor"):
    instructor_id: str

class BookCallback(CallbackData, prefix="book"):
    book_id: str

class DownloadCallback(CallbackData, prefix="download_b"):
    book_id: str

class ChapterCallback(CallbackData, prefix="chapter"):
    course_id: str

class ChapterInfoCallback(CallbackData, prefix="chapter_info"):
    chapter_id: str
