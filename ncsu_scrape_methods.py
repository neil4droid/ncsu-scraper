from ncsu_course import CourseSection
from typing import Tuple
from typing import List
from bs4 import Tag


def get_course_id(section: Tag) -> str:
	if not section: return None
	if not section.h1 or not section.h1.contents: return None
	return section.h1.contents[0].strip()

def get_course_name(section: Tag) -> str:
	if not section: return None
	if not section.h1 or not section.h1.contents: return None

	return section.h1.small.string.strip()

def get_course_credits_tuple(section: Tag) -> Tuple[int, int]:
    if not section: return None
    if not section.h1 or not section.h1.contents: return None

    credits_range_arr = section.h1.span.string.split(":")[1].split("-")
    if not credits_range_arr: return None
    
    min_creds = int(credits_range_arr[0].strip())
    if len(credits_range_arr) == 1: max_creds = min_creds
    else: max_creds = int(credits_range_arr[1].strip())

    return (min_creds, max_creds)

def get_course_prereqs(section: Tag) -> List[str]:
    if not section: return None

    return None

def get_course_sections_list(section: Tag) -> List[CourseSection]:
	if not section: return None
	section_table = section.find("table", class_="section-table")
	if not section_table or not section_table.tr: return None

	course_section_list = []
	for child in section_table.children:
		if child.name != "tr": continue
		row = child
		if not row.contents: continue
		course_section = CourseSection()
		course_section.section = row.contents[0].string.strip() if row.contents[0].string else None
		course_section.component = row.contents[1].string.strip() if len(row.contents) > 1 and row.contents[1].string else None
		course_section.class_number = row.contents[2].string.strip() if len(row.contents) > 2 and row.contents[2].string else None
		course_section.location = row.contents[5].string.strip() if len(row.contents) > 5 and row.contents[5].string else None
		course_section.instructor = row.contents[6].a.string.strip() if len(row.contents) > 6 and row.contents[6].a else row.contents[6].string.strip()
		course_section.begin_date = row.contents[7].string.split("-")[0].strip() if len(row.contents) > 7 and row.contents[7].string else None
		course_section.end_date = row.contents[7].string.split("-")[1].strip() if len(row.contents) > 7 and row.contents[7].string and len(row.contents[7].string.split("-")) > 1 else None
		course_section.course_section_status = row.contents[3].span.string.strip() if len(row.contents) > 3 and row.contents[3].span and row.contents[3].span.string else None
		course_section.available_seats = row.contents[3].contents[2].string.split("/")[0].strip() if len(row.contents) > 3 and row.contents[3].contents and len(row.contents[3].contents) > 2 and row.contents[3].contents[2].string else None
		course_section.total_seats = row.contents[3].contents[2].string.split("/")[1].strip() if len(row.contents) > 3 and row.contents[3].contents and len(row.contents[3].contents) >2 and row.contents[3].contents[2].string and len(row.contents[3].contents[2].string.split("/")) > 1 else None

		course_section_list.append(course_section)
	
	return course_section_list