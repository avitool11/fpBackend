import psycopg2
from flask import jsonify
import base64

def getConnectionDetails():
  conn = psycopg2.connect(
    host="35.244.45.154",
    database="final-project",
    user="postgres",
    password="avi2014#"
    )
  return conn

def registrationHandler(name,email,password,role,dob):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "INSERT INTO user_details (name, email, password, role, verified, dob) VALUES (%s, %s, %s, %s, %s, %s)"
  values = (name,email,password,role,False,dob)
  try:
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    cur.close()
    conn.close()
    print(e)
    return False
  
def loginHandler(email,password):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "Select * from user_details where email = %s"
  values = (email,)
  try:
    r = cur.execute(query,values)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows[0][-4] == password:
        return rows
    else:
        return False
  except Exception as e:
    print(e)
    cur.close()
    conn.close()
    return False

def checkRole(userId, role):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "Select * from user_details where id = %s"
  values = (userId,)
  try:
    r = cur.execute(query,values)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows[0][-3] == role:
      return True
    else:
      return False
  except Exception as e:
    print(e)
    cur.close()
    conn.close()
    return False
  
def getDueApprovals(userId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be ADMIN"
  else:
    return dueApprovals()

def dueApprovals():
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "Select * from user_details where verified = %s"
  values = (False,)
  try:
    r = cur.execute(query,values)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
  except:
    cur.close()
    conn.close()
    return False

def approvalHandler(userIds, adminId):
  d = checkRole(adminId,"admin")
  if d == False:
    return "USER MUST BE ADMIN"
  for userId in userIds:
    g = approveUser(userId)
    h = assignTable(userId)
    if g == False :
      return False
  return True
  
def assignTable(userId):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "Select * from user_details where id = %s"
  values = (userId,)
  r = cur.execute(query,values)
  rows = cur.fetchall()
  row = rows[0]
  role = row[-3]
  if role == "faculty":
    query = "Insert INTO faculties (user_id) values (%s)"
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  elif role == "student":
    query = "INSERT INTO students (user_id) values (%s)"
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  return True

def approveUser(userId):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "UPDATE user_details SET verified = %s WHERE id = %s"
  values = (True,userId)
  try: 
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    cur.close()
    conn.close()
    return False

def editProfile(userId,oldPassword,newPassword):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "select * from user_details where id = %s"
  values = (userId,)
  try:
    r = cur.execute(query,values)
    rows = cur.fetchall()
    if rows[0][-4] == oldPassword:
      queryNew = "Update user_details SET password = %s where id = %s"
      valuesnew = (newPassword,userId)
      r = cur.execute(queryNew,valuesnew)
      conn.commit()
      cur.close()
      conn.close()
      return True
  except Exception as e:
    print(e)
    cur.close()
    conn.close()
    return False
  
def assignAssignment(userId, questions, batchId, courseId):
  
  questions = "##;;".join(questions)
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be Faculty"
  else:
    try:
      conn = getConnectionDetails()
      cur = conn.cursor()
      query = "Insert into assignment (description,faculty_id,batch_id,course_id) values (%s,%s,%s,%s)"
      values = (questions,userId,batchId,courseId)
      r = cur.execute(query,values)
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      return False

def getFacultyBatchCourseDetails(userId):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  else:
    try:
      conn = getConnectionDetails()
      cur = conn.cursor()
      query = "Select * from faculties where user_id = %s"
      values = (userId,)
      r = cur.execute(query,values)
      rows = cur.fetchall()
      print(rows)
      row = rows[0]
      batches = row[-2]
      courses = row[-1]
      print(batches,courses)
      batch = resolveBatches(batches)
      course = resolveCourses(courses)
      return (batch,course)
    except Exception as e:
      print(e)
      return False

def resolveBatches(batches):
  batchDetails = []
  for batch in batches:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from batch where id = %s"
    values = (batch,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    row = rows[0]
    j = {}
    j['batch_id'] = row[0]
    j['batch_code'] = row[1]
    j['batch_name'] = row[2]
    batchDetails.append(j)
    cur.close()
    conn.close()
  return ({"batches":batchDetails})

def resolveCourses(courses):
  courseDetails = []
  for course in courses:
    j = getSingleCourseDetails(course)
    courseDetails.append(j)
  return ({"courses":courseDetails})

def getSingleCourseDetails(course):
  conn = getConnectionDetails()
  cur = conn.cursor()
  query = "Select * from course where id = %s"
  values = (course,)
  r = cur.execute(query,values)
  rows = cur.fetchall()
  row = rows[0]
  j = {}
  j['course_id'] = row[0]
  j['course_code'] = row[1]
  j['course_name'] = row[2]
  cur.close()
  conn.close()
  return j

def viewAssignment(userId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  else:
    try:
      conn = getConnectionDetails()
      cur = conn.cursor()
      query = "Select * from students where user_id = %s"
      values = (userId,)
      r = cur.execute(query,values)
      rows = cur.fetchall()
      row = rows[0]
      batchId = row[-1]
      print(batchId)
      queryNew = "Select * from assignment where batch_id = %s"
      valueNew = (batchId,)
      r = cur.execute(queryNew,valueNew)
      rows = cur.fetchall()
      fOutput = []
      for row in rows:
        course = row[-1]
        description = row[1]
        questions = description.split("##;;")
        j = {}
        j["questions"] = questions
        j["course"] = getSingleCourseDetails(course)
        fOutput.append(j)
      return fOutput
    except Exception as e:
      return False

def getAllCourses(userId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User Must be Admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "SELECT * from courses"
    rows = query.execute()
    result = []
    for row in rows:
      j = {}
      j['course_id'] = row[0]
      j['course_code'] = row[1]
      j['course_name'] = row[2]
      result.append(j)
    cur.close()
    conn.close()
    return result
  except:
    cur.close()
    conn.close()
    return False
  
def addNewCourse(userId,courseCode,courseName):
  d = checkRole(userId, "admin")
  if d == False:
    return "User must be admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "INSERT INTO course (code, name) VALUES (%s, %s)"
    values = (courseCode,courseName)
    r = cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except:
    return False    

def uploadNotice(userId, batchId, courseId, noticeData):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be a staff"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "INSERT INTO notice (description, course_id, batch_id, faculty_id) values (%s, %s, %s, %s)"
    values = (noticeData, courseId, batchId, userId)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except:
    cur.close()
    conn.close()
    return False
  
def uploadFeedback(userId, courseId, feedback):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be a student"
  try:
    query = "INSERT INTO feedback (content, student_id , course_id) VALUES (%s, %s, %s)"
    values = (feedback, userId, courseId)
    conn = getConnectionDetails()
    cur = conn.cursor()
    r = cur.execute(query,values)
    conn.commit()
    conn.close()
    cur.close()
    return True
  except:
    return False
  
def getAllCourses(userId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User Must be Admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "SELECT * from course"
    r = cur.execute(query)
    rows = cur.fetchall()
    result = []
    for row in rows:
      j = {}
      j['course_id'] = row[0]
      j['course_code'] = row[1]
      j['course_name'] = row[2]
      result.append(j)
    cur.close()
    conn.close()
    return result
  except Exception as e:
    print(e)
    cur.close()
    conn.close()
    return False

def assignCourse(userId,courseId,facultyId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be admin"
  facultyCourse = getFacultyBatchCourseDetails(facultyId)
  courseDetails = facultyCourse[1]
  courseIds = []
  for course in courseDetails:
    courseIds.append(course["course_id"])
  courseIds = set(courseIds)
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Update faculties set course_id = %s where user_id = %s"
    values = (courseId,facultyId)
    r = cur.execute(query,values)
    conn.commit()
    conn.close()
    cur.close()
    return True
  except Exception as e:
    return False
  
def getFacultyStudents(userId):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  else:
    try:
      conn = getConnectionDetails()
      cur = conn.cursor()
      query = "Select * from faculties where user_id = %s"
      values = (userId,)
      r = cur.execute(query,values)
      rows = cur.fetchall()
      row = rows[0]
      batches = row[-2]
      students = getStudents(batches)
      return students
    except Exception as e:
      print(e)
      return False
    
def getStudents(batches):
  students = []
  for batch in batches:
    # print(batch)
    try:
       conn = getConnectionDetails()
       cur = conn.cursor()
       query = "Select * from students where batch_id = %s"
       values = (batch,)
       r = cur.execute(query,values)
       rows = cur.fetchall()
      #  print(rows)
       for row in rows:
         students.append(getUserDetails(row[1]))
       cur.close()
       conn.close()
       
    except Exception as e:
      # print(e)
      return False
  return students
    
def getUserDetails(userId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where id = %s"
    values = (userId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    row = rows[0]
    j = {}
    j['user_id'] = row[0]
    j['user_name'] = row[1]
    j['user_email'] = row[2]
    j['user_dob'] = row[6]
    cur.close()
    conn.close()
    return j
  except Exception as e:
    print(e)
    return False
  
def updateStudentDetails(userId,studentId,email,dob,name):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Update user_details set email = %s, dob = %s, name = %s where id = %s"
    values = (email,dob,name,studentId)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e: 
    print(e)
    return False
  
def deleteStudent(userId,studentId):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Delete from user_details where id = %s"
    values = (studentId,)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def getStudentBatchCourseDetails(userId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from students where user_id = %s"
    values = (userId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    row = rows[0]
    batch = row[-1]
    course = getCourseDetailsFromBatch(batch)
    return course
  except Exception as e:
    print(e)
    return False
  
def getCourseDetailsFromBatch(batchId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from batch where batch_id = %s"
    values = (batchId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    courses = rows[-1]
    courseDetails = resolveCourses(courses)
    return courseDetails
  except Exception as e:
    print(e)
    return False
  
def viewAttendance(userId,courseId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    batch_id = getStudentBatch(userId)
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from attendance where batch_id = %s and course_id = %s"
    values = (batch_id,courseId)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    # row = rows[0]
    return rows
  except Exception as e:
    print(e)
    return False

def getStudentBatch(userId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select batch_id from students where user_id = %s"
    values = (userId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    row = rows[0]
    batch_id = row[2]
    return batch_id
  except Exception as e:
    print(e)
    return False
  
def getResult(userId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    batch_id = getStudentBatch(userId)
    courseId = getStudentBatchCourseDetails(userId)
    query = "Select * from result where batch_id = %s and course_id = %s"
    values = (batch_id,courseId)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    return rows
  except Exception as e:
    print(e)
    return False
  
def uploadAttendance(userId,batch_id,course_id,date,students_list,attendance_list):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Insert into attendance (batch_id, course_id, date, students_list, attendance_list) VALUES (%s, %s, %s, %s, %s)"
    values = (batch_id, course_id, date, students_list, attendance_list)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def getAllBatchCourseDetails():
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from batch"
    r = cur.execute(query)
    rows = cur.fetchall()
    result = []
    for row in rows:
      j = {}
      j['batch_id'] = row[0]
      j['batch_code'] = row[1]
      j['batch_name'] = row[2]
      courses = row[-1]
      courses = resolveCourses(courses)
      j['courses'] = courses
      result.append(j)
    cur.close()
    conn.close()
    return result
  except Exception as e:
    print(e)
    cur.close()
    conn.close()
    return False
  
def viewNotice(batchId,courseId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from notice where batch_id = %s and course_id = %s"
    values = (batchId,courseId)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    return rows
  except Exception as e:
    print(e)
    return False
  
def uploadExternalResult(userId, data,batchId,courseId):
  d = checkRole(userId,"staff")
  if d == False:
    return "User must be staff"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    byte_array = base64.b64decode(data.split(',')[1])
    query = "Insert into result (batch_id, course_id, content, is_external, staff_id) VALUES (%s, %s, %s, %s, %s)"
    values = (batchId, courseId, byte_array, True, userId)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def uploadInternalResult(userId, data,batchId,courseId):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    byte_array = base64.b64decode(data.split(',')[1])
    query = "Insert into result (batch_id, course_id, content, is_external, staff_id) VALUES (%s, %s, %s, %s, %s)"
    values = (batchId, courseId, byte_array, False, userId)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def uploadTimetable(userId, data,batchId,courseId):
  d = checkRole(userId,"staff")
  if d == False:
    return "User must be staff"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    byte_array = base64.b64decode(data.split(',')[1])
    query = "Insert into timetable (batch_id, content, staff_id) VALUES (%s, %s, %s)"
    values = (batchId, byte_array, userId)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def viewTimetable(userId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    batchId = getStudentBatch(userId)
    query = "Select * from timetable where batch_id = %s"
    values = (batchId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows[0]
  except Exception as e:
    print(e)
    return False
  
# print(getStudentBatchCourseDetails(4))