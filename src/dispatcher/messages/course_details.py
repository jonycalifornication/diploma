from src.services.schemas.schemas import CourseInfo, InstructorInfo, BookInfo


async def course_details(course: CourseInfo):
    return (
        f"📚 <b>{course.title}</b>\n\n"
        f"📝 <b>Описание:</b> {course.description or 'Нет описания'}\n\n"
        f"⏰ <b>Длительность:</b> {course.duration} часов\n"
        f"🏷️ <b>Теги:</b> {course.tags or 'Нет тегов'}\n"
        f"👨‍🏫 <b>Преподаватель:</b> {course.instructor.name or 'Не указан'}\n\n"
    )


async def instructor_details(instructor: InstructorInfo):
    return (
        f"📚 <b>{instructor.name}</b>\n\n"
        f"📝 <b>Био:</b> {instructor.bio or 'Нет Био'}\n\n"
        f"⏰ <b>Степень:</b> {instructor.degree}\n"
        f"🏷️ <b>Специализация:</b> {instructor.specialization}\n"
    )

async def book_details(book: BookInfo):
    return (
        f"📚 <b>{book.book_title}</b>\n\n"
        f"📝 <b>Автор:</b> {book.author}\n\n"
        f"⏰ <b>Рейтинг:</b> {book.rating}\n"
    )