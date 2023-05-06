import psycopg2
from flask import jsonify

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
  