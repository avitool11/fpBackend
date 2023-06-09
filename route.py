from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
import handlers as handler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(app)


@app.route("/",methods=['GET'])
def healthCheck():
    return jsonify({"result":"Hello World"})

@app.route('/registration',methods = ['POST'])
def registration(): #Done
    if request.method == 'POST':
        print("Incoming Request")
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        role = request.json['role']
        dob = request.json['dob']
        return jsonify({"result":handler.registrationHandler(name,email,password,role,dob)})

@app.route('/login',methods = ['POST'])
def login(): #Done
    email = request.json['email']     
    password = request.json['password']
    return jsonify({"result":handler.loginHandler(email,password)})

@app.route('/approval',methods = ['POST','GET'])
def approvalAdmin(): #Done
    if request.method == 'POST':
        userId = int(int(request.json['user_id']))
        adminId = int(request.json ['admin_id'])
        return jsonify({"result":handler.approvalHandler(userId,adminId)})
    if request.method == 'GET':
        adminId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getDueApprovals(adminId)}) 
@app.route('/editProfile', methods = ['POST'])
def editProfile(): #Done
    userId = int(int(request.json['user_id']))
    passwordOld = request.json['old_password']
    passwordNew = request.json['new_password']
    return jsonify({"result":handler.editProfile(userId,passwordOld,passwordNew)})

@app.route('/assignment', methods =['GET','POST'])
def assignAssignment(): #Done
    if request.method == 'POST':
        userId = int(int(request.json['user_id']))
        questions = request.json['questions']
        batchId = int(request.json['batch'])
        courseId = int(request.json['course'])
        return jsonify({"result":handler.assignAssignment(userId, questions, batchId, courseId)})
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        # print(userId)
        return jsonify({"result":handler.getFacultyBatchCourseDetails(userId)})

@app.route('/viewAssignment', methods=['GET'])
def viewAssignment(): #Done
    userId = int(request.args.get('user_id'))
    return jsonify({"result":handler.viewAssignment(userId)})

@app.route('/viewTimetable', methods=['GET'])
def viewTimetable(): #Done
    userId = int(request.args.get('user_id'))
    return jsonify({"result":handler.viewTimetable(userId)})

@app.route('/uploadTimetable', methods=['POST'])
def uploadTimetable(): #Done
    userId = int(int(request.json['user_id']))
    data = request.json['data']
    # courseId = int(request.json['course_id'])
    batchId = int(request.json['batch_id'])
    return jsonify({"result":handler.uploadTimetable(userId,data,batchId)})

@app.route('/feedback', methods =['POST','GET'])
def uploadFeedback(): #Done
    if request.method == 'POST':
        userId = int(int(request.json['user_id']))
        courseId = int(request.json['course_id'])
        feedback = request.json ['feedback']
        return jsonify({"result":handler.uploadFeedback(userId,courseId,feedback)})
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getStudentBatchCourseDetails(userId)}) 

@app.route('/uploadInternalResult', methods = ['POST','GET'])
def uploadInternalResult(): #Done
    if request.method == 'POST':
        userId = int(int(request.json['user_id']))
        data = request.json['data']
        batchId = int(request.json['batch_id'])
        courseId = int(request.json['course_id'])
        return jsonify({"result":handler.uploadInternalResult(userId,data,batchId,courseId)}) 
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))         
        return jsonify({"result":handler.getFacultyBatchCourseDetails(userId)})

@app.route('/uploadExternalResult', methods = ['POST', 'GET'])
def uploadExternalResult(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        data = request.json['data']
        batchId = int(request.json['batch_id'])
        courseId = int(request.json['course_id'])
        return jsonify({"result":handler.uploadExternalResult(userId,data,batchId,courseId)})
    if request.method == 'GET':
        return jsonify({"result":handler.getAllBatchCourseDetails()}) 

@app.route('/notice', methods = ['POST','GET'])
def uploadNotice(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        batchId = int(request.json['batch_id'])
        courseId = int(request.json['course_id'])
        noticeData = request.json['notice_data']
        return jsonify({"result":handler.uploadNotice(userId,batchId,courseId,noticeData)})
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))       
        return jsonify({"result":handler.getFacultyBatchCourseDetails(userId)})

@app.route('/viewNotice',methods = ['POST','GET'])
def viewNotice(): #Done
    if request.method == 'POST':
        batchId = int(request.json['batch_id'])
        courseId = int(request.json['course_id'])
        return jsonify({"result":handler.viewNotice(batchId,courseId)})
    if request.method == 'GET':
        return jsonify({"result":handler.getAllBatchCourseDetails()}) 

@app.route('/uploadAttendance',methods=['POST','GET'])
def attendanceDetails(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        # batchId = int(request.json['batch_id'])
        courseId = int(request.json['course_id'])
        date = request.json['date']
        students_list = request.json['students_list']
        attendace_list = request.json['attendance_list']
        return jsonify({"result":handler.uploadAttendance(userId,courseId,date,students_list,attendace_list)})

    if request.method == 'GET':
        courseId = request.args.get('course_id')
        # print(courseId)
        return jsonify({"result":handler.getAllStudentsofCourse(courseId)}) 

@app.route('/viewResult',methods = ['POST'])
def resultDetails(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        couresId = int(request.json['course_id'])
        return jsonify({"result":handler.getResult(userId,couresId)}) 

@app.route('/viewAttendance', methods = ['POST','GET'])
def viewAttendance(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        courseId = int(request.json['course_id'])
        return jsonify({"result":handler.viewAttendance(userId,courseId)})
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getStudentBatchCourseDetails(userId)}) 

@app.route('/editStudentDetails', methods = ['POST','GET','PUT'])
def updateStudentDetails(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        studentId = int(request.json['student_id'])
        email = request.json['new_email']
        dob = request.json['dob']
        name = request.json['name']
        return jsonify({"result":handler.updateStudentDetails(userId,studentId,email,dob,name)}) #This POST request will Update the student details
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getFacultyStudents(userId)}) #A Faculty can change Student Details. This GET request will fetch all the students under the faculty
    if request.method == 'PUT': 
        userId = int(request.json['user_id'])
        studentId = int(request.json['student_id'])
        return jsonify({"result":handler.deleteStudent(userId,studentId)}) #This Delete request will delete the user})

@app.route('/addCourse', methods = ['POST'])
def addCourse(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        courseName = request.json['course_name']
        courseCode = request.json['course_code']
        return jsonify({"result":handler.addNewCourse(userId,courseCode,courseName)})
    
@app.route('/assignCourse', methods = ['POST','GET','PUT'])
def assignCourse(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        courseCode = int(request.json['course_id'])
        facultyId = int(request.json['faculty_id'])
        return jsonify({"result":handler.assignCourse(userId,courseCode,facultyId)})
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getAllCourses(userId)})
    if request.method == 'PUT':
        userId = int(request.json['user_id'])
        courseCode = int(request.json['course_id'])
        batchId = int(request.json['batch_id'])
        return jsonify({"result":handler.addNewCourseToBatch(userId,batchId,courseCode)})

@app.route('/assignBatch', methods = ['POST','GET'])
def assignBatch(): #Done
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        batchId = int(request.json['batch_id'])
        id = int(request.json['id'])
        to = request.json['assign_to']
        if to == "student":
            return jsonify({"result":handler.assignBatchStudent(userId,batchId,id)})
        else:
            return jsonify({"result":handler.assignBatch(userId,batchId,id)})
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getAllBatches(userId)})
@app.route('/addBatch', methods = ['POST'])
def addBatch():
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        batchName = request.json['batch_name']
        batchCode = request.json['batch_code']
        return jsonify({"result":handler.addNewBatch(userId,batchCode,batchName)})
    
@app.route('/addPlacementCompany', methods = ['POST'])
def addCompany():
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        companyCode = request.json['company_name']
        role = request.json['role']
        ctc = request.json['ctc']
        return jsonify({"result":handler.addNewPlacementCompany(userId,companyCode,role,ctc)})
    
@app.route('/addPlacement', methods = ['POST','GET'])
def addPlacement():
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        companyCode = int(request.json['placement_id'])
        studentId = int(request.json['student_id'])
        return jsonify({"result":handler.addNewPlacement(userId,companyCode,studentId)})
    if request.method == 'GET':
        return jsonify({"result":handler.getAllPlacementCompany()})
    
@app.route('/viewPlacement', methods = ['GET'])
def viewPlacement():
    if request.method == 'GET':
        userId = int(request.args.get('user_id'))
        return jsonify({"result":handler.getUserPlacements(userId)})

@app.route('/getAllStudents', methods = ['GET'])
def getAllStudents():
    return jsonify({"result":handler.getAllStudents()})

@app.route('/getAllStudentswithoutBatch', methods = ['GET'])
def getAllStudentswithoutBatch():
    return jsonify({"result":handler.getAllStudentswithoutBatch()})

@app.route('/getAllFaculties', methods = ['GET'])
def getAllFaculties():
    return jsonify({"result":handler.getAllFaculties()})

@app.route('/getAllFeedbacks', methods = ['POST'])
def getAllFeedbacks():
    if request.method == 'POST':
        userId = int(request.json['user_id'])
        return jsonify({"result":handler.getAllFeedbacks(userId)})
    
if __name__ == '__main__':
    app.run()
