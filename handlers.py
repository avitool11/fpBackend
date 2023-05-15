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
  # conn = psycopg2.connect(
  #   host="localhost",
  #   database="adeena",
  #   user="postgres",
  #   password="2019"
  #   )
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
    try: 
      conn = getConnectionDetails()
      cur = conn.cursor()
      query = "Select * from user_details where id = %s"
      values = (userId,)
      r = cur.execute(query,values)
      rows = cur.fetchall()
      row = rows[0]
      if row[-2] == True:
        return "One of the User already approved. Hit get due approvals"
      conn.close()
      cur.close()
    except Exception as e:
      print(e)

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
      query = "Insert into assignment (description,faculty_id,batch,course_id) values (%s,%s,%s,%s)"
      values = (questions,userId,batchId,courseId)
      r = cur.execute(query,values)
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
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
      if row[-2] == None:
        batches = {"batches":[]}
      else:
        batches = row[-2]
        batches = resolveBatches(batches)
      if row[-1] == None:
        courses = {"courses":[]}
      else:
        courses = row[-1] 
        courses = resolveCourses(courses)
      # print(batches,courses)
      
      return (batches,courses)
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
    # print(course)
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
      # print(batchId)
      queryNew = "Select * from assignment where batch = %s"
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
      print(e)
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
  
def getAllBatches(userId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User Must be Admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "SELECT * from batch"
    r = cur.execute(query)
    rows = cur.fetchall()
    result = []
    for row in rows:
      j = {}
      j['batch_id'] = row[0]
      j['batch_code'] = row[1]
      j['batch_name'] = row[2]
      j['batch_courses'] = row[3]
      result.append(j)
    cur.close()
    conn.close()
    return result
  except Exception as e:
    print(e)
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
    return "User must be a faculty"
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
  except Exception as e:
    print(e)
    return False
  
# def getAllCourses(userId):
#   d = checkRole(userId,"admin")
#   if d == False:
#     return "User Must be Admin"
#   try:
#     conn = getConnectionDetails()
#     cur = conn.cursor()
#     query = "SELECT * from course"
#     r = cur.execute(query)
#     rows = cur.fetchall()
#     result = []
#     for row in rows:
#       j = {}
#       j['course_id'] = row[0]
#       j['course_code'] = row[1]
#       j['course_name'] = row[2]
#       result.append(j)
#     cur.close()
#     conn.close()
#     return result
#   except Exception as e:
#     print(e)
#     cur.close()
#     conn.close()
#     return False

def assignCourse(userId,courseId,facultyId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be admin"
  facultyCourse = getFacultyBatchCourseDetails(facultyId)
  courseDetails = facultyCourse[1]
  print(courseDetails)
  courseDetails = courseDetails['courses']
  courseIds = []
  for course in courseDetails:
    courseIds.append(course["course_id"])
  courseIds.append(courseId)
  # courseIds = set(courseIds)
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Update faculties set course_id = %s where user_id = %s"
    values = (courseIds,facultyId)
    r = cur.execute(query,values)
    conn.commit()
    conn.close()
    cur.close()
    return True
  except Exception as e:
    return False
  
def assignBatch(userId,batchId,facultyId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be admin"
  facultyBatch = getFacultyBatchCourseDetails(facultyId)
  # print(facultyBatch)
  batchDetails = facultyBatch[0]
  batchDetails = batchDetails['batches']
  print(batchDetails)
  batchIds = []
  for batch in batchDetails:
    batchIds.append(batch["batch_id"])
  batchIds.append(batchId)
  # batchIds = set(batchIds)
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Update faculties set batch_id = %s where user_id = %s"
    values = (batchIds,facultyId)
    r = cur.execute(query,values)
    conn.commit()
    conn.close()
    cur.close()
    return True
  except Exception as e:
    print(e)
    return False

def assignBatchStudent(userId,batchId,studentId):
  d = checkRole(userId,"staff")
  if d == False:
    return "User must be staff"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Update students set batch_id = %s where user_id = %s"
    values = (batchId,studentId)
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
    query1 = "Delete from students where user_id = %s"
    values = (studentId,)
    r = cur.execute(query1,values)
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
    query = "Select * from batch where id = %s"
    values = (batchId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    courses = rows[0][-1]
    if courses == None:
      courses = []
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
    query = "Select * from attendance where course_id = %s"
    values = (courseId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    # row = rows[0]
    rdl = []
    for row in rows:
      resultDict = {"course_id":row[1],"studentList":row[2],"attendanceList":row[3]}
      rdl.append(resultDict)
    return rdl
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
    query = "Select * from students where user_id = %s"
    values = (userId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    row = rows[0]
    # print(rows)
    batch_id = row[2]
    return batch_id
  except Exception as e:
    print(e)
    return False
  
def getResult(userId,courseId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    batch_id = getStudentBatch(userId)
    # print(batch_id,courseId)
    query = "Select * from result where batch_id = %s and course_id = %s"
    values = (batch_id,courseId)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    rows1 = []
    
    for row in rows:
      bytea_data = row[1].tobytes()
      base64_data = base64.b64encode(bytea_data)
      row = list(row)
      row[1] = base64_data.decode()
      resultDict = {"resultImage":row[1],"batchId": row[2],"courseId": row[3], "isExternal": row[4]}
      rows1.append(resultDict)
    # print(rows)
    return rows1
  except Exception as e:
    print(e)
    return False
  
def uploadAttendance(userId,course_id,date,students_list,attendance_list):
  d = checkRole(userId,"faculty")
  if d == False:
    return "User must be faculty"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Insert into attendance (course_id, date, student_list, attendance_list) VALUES ( %s, %s, %s, %s)"
    values = (course_id, date, students_list, attendance_list)
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
    rdl = []
    for row in rows:
      resultDict = {"course_id":row[2],"notice":row[1],"batchId":row[3]}
      rdl.append(resultDict)
    return rdl
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
  
def uploadTimetable(userId, data,batchId):
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
    row = rows[0]
    bytea_data = row[1].tobytes()
    base64_data = base64.b64encode(bytea_data)
    row = list(row)
    row[1] = base64_data.decode()
    row = tuple(row)
    resultDict = {"timetable":row[1],"batchId":row[2]}
    cur.close()
    conn.close()
    return resultDict
  except Exception as e:
    print(e)
    return False
  
def addNewBatch(userId,batch_code,batch_name):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Insert into batch (code, batch_name) VALUES (%s, %s)"
    values = (batch_code, batch_name)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def addNewCourseToBatch(userId,batch_id,course_id):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    courses = getCourseDetailsFromBatch(batch_id)
    courses = courses['courses']
    cl = []
    for course in courses:
      cl.append(course['course_id'])
    cl.append(course_id)
    print(cl)
    # cl = set(cl)
    query = "Update batch set course_id = %s where id = %s"
    values = (cl, batch_id)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def getAllStudentsofCourse(courseId):
  courseId = int(courseId)
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from batch"
    # values = (courseId,)
    r = cur.execute(query)
    rows = cur.fetchall()
    # print(rows)
    batchIds = []
    for row in rows:
      if (inCourse(row[-1],courseId)):
        batchIds.append(row[0])
    # print(batchIds)
    queryNew = "SELECT * FROM students WHERE batch_id = ANY(%s)"
    valuesnew = (batchIds,) 
    r = cur.execute(queryNew,valuesnew)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    studentIdList = []
    for row in rows:
      studentDetails = getStudentDetails(row[0])
      k = {}
      k['student_user_id'] = studentDetails[0]
      k['student_name'] = studentDetails[1]
      k['student_email'] = studentDetails[2]
      # k['student_batch'] = getStudentBatch(studentDetails[0])
      studentIdList.append(k)
    # print(studentIdList)
    return studentIdList
  except Exception as e:
    print(e)
    return False
  
def inCourse(course,courseId):
  if courseId in course:
    return True
  return False

def addNewPlacementCompany(userId,companyCode,role,ctc):
  d = checkRole(userId,"staff")
  if d == False:
    return "User must be staff"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Insert into placement_companies (company_name, role, ctc) VALUES (%s, %s, %s)"
    values = (companyCode, role, ctc)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def getAllPlacementCompany():
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from placement_companies"
    r = cur.execute(query)
    rows = cur.fetchall()
    result = []
    for row in rows:
      j = {}
      j['company_code'] = row[0]
      j['role'] = row[1]
      j['ctc'] = row[3]
      j['company_name'] = row[2]
      result.append(j)
    cur.close()
    conn.close()
    return result
  except Exception as e:
    print(e)
    return False
  
def addNewPlacement(userId,companyId,studentId):
  d = checkRole(userId,"staff")
  if d == False:
    return "User must be staff"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Insert into placement_records (placement_id, student_id) VALUES (%s, %s)"
    values = (companyId, studentId)
    r = cur.execute(query,values)
    conn.commit()
    cur.close()
    conn.close()
    return True
  except Exception as e:
    print(e)
    return False
  
def getUserPlacements(userId):
  d = checkRole(userId,"student")
  if d == False:
    return "User must be student"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from placement_records where student_id = %s"
    values = (userId,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    fresult = []
    for row in rows:
      c = resolveCompanyDetails(row[-1])
      j = {}
      j['company_name'] = c['company_name']
      j['role'] = c['role']
      j['ctc'] = c['ctc']
      fresult.append(j)
    cur.close()
    conn.close()
    return fresult
  except Exception as e:
    print(e)
    return False
  
def resolveCompanyDetails(companyId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from placement_companies where id = %s"
    values = (companyId,)
    r = cur.execute(query,values)
    row = cur.fetchone()
    c = {}
    c['company_name'] = row[2]
    c['role'] = row[1]
    c['ctc'] = row[3]
    cur.close()
    conn.close()
    return c
  except Exception as e:
    print(e)
    return False

def getAllFaculties():
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where role = 'faculty'"
    r = cur.execute(query)
    rows = cur.fetchall()
    
    return rows
  except Exception as e:
    print(e)
    return False
  
def getAllStudents():
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where role ='student'"
    r = cur.execute(query)
    rows = cur.fetchall()
    return rows
  except Exception as e:
    print(e)
    return False
  
def getAllStudentswithoutBatch():
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from students"
    r = cur.execute(query)
    rows = cur.fetchall()
    studentIds = []
    for row in rows:
      if row[-1] == None:
        studentIds.append(row[1])  
  except Exception as e:
    print(e)
    return False
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where role ='student'"
    r = cur.execute(query)
    rows = cur.fetchall()
    studentIds1 = []
    for row in rows:
      studentIds1.append(row[0])
  except Exception as e:
    print(e)
    return False
  studentsIds2 = list(set(studentIds) & set(studentIds1))
  # list(studentsIds2)
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where id = ANY(%s)"
    values = (studentsIds2,)
    r = cur.execute(query,values)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
  except Exception as e:
    print(e)
    return False
  
def getAllFeedbacks(userId):
  d = checkRole(userId,"admin")
  if d == False:
    return "User must be admin"
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from feedback"
    result = []
    r = cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
      j = {}
      j['feedback'] = row[1]
      studentDetails = getStudentDetails(row[2])
      k = {}
      k['student_user_id'] = studentDetails[0]
      k['student_name'] = studentDetails[1]
      k['student_email'] = studentDetails[2]
      k['student_batch'] = getStudentBatch(studentDetails[0])
      courseDetails = getSingleCourseDetails((row[3]))
      j['course_details'] = courseDetails
      j['student_details'] = k
      facultyId = resolveFaculty( k['student_batch'], j['course_details']['course_id'])
      q = getFacultyDetails(facultyId)
      j['faculty_details'] = q
      result.append(j)
    conn.close()
    cur.close()
    return (result)
  except Exception as e:
    print(e)
    return False
  
def getStudentDetails(studentId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where id = %s"
    values = (studentId,)
    r = cur.execute(query,values)
    row = cur.fetchone()
    return row
  except Exception as e:
    print(e)
    return False
  
def getFacultyDetails(facultyId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from user_details where id = %s"
    values = (facultyId,)
    r = cur.execute(query,values)
    row = cur.fetchone()
    k = {}
    k['faculty_user_id'] = row[0]
    k['faculty_name'] = row[1]
    k['faculty_email'] = row[2]
    return k
  except Exception as e:
    print(e)
    return False
  
def resolveFaculty(batchId, courseId):
  try:
    conn = getConnectionDetails()
    cur = conn.cursor()
    query = "Select * from faculties"
    r = cur.execute(query)
    rows = cur.fetchall()
    # print(rows)
    for row in rows:
      courses = row[-1]
      batches = row[-2]
      if courses == None or batches == None:
        continue
      if batchId in batches and courseId in courses:
        conn.close()
        cur.close() 
        return row[1]
    conn.close()
    cur.close()
    return "No Faculty Found"
    
  except Exception as e:
    print(e)
    return False
  
# print(getAllPlacementCompany())