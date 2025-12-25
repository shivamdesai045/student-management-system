from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Data file to store students
DATA_FILE = 'students.json'

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def load_students():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }

        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }

        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .students-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .students-table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }

        .students-table td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }

        .students-table tr:hover {
            background: #f8f9ff;
        }

        .action-btn {
            padding: 6px 15px;
            margin-right: 8px;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
        }

        .edit-btn {
            background: #4CAF50;
        }

        .delete-btn {
            background: #f44336;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state-icon {
            font-size: 60px;
            margin-bottom: 20px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            color: #666;
            margin-top: 10px;
            font-size: 0.9em;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }

        .modal-content {
            background: white;
            max-width: 600px;
            margin: 100px auto;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .close {
            font-size: 30px;
            cursor: pointer;
            color: #999;
        }

        .close:hover {
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 Student Management System</h1>
            <p class="subtitle">Manage your students efficiently</p>
        </header>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ students|length }}</div>
                <div class="stat-label">Total Students</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ students|selectattr('grade', 'equalto', 'A')|list|length }}</div>
                <div class="stat-label">Grade A Students</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ courses|length if courses else 0 }}</div>
                <div class="stat-label">Active Courses</div>
            </div>
        </div>

        <div class="card">
            <h2 style="margin-bottom: 20px; color: #333;">➕ Add New Student</h2>
            <form method="POST" action="/add">
                <div class="form-row">
                    <div class="form-group">
                        <label for="name">Full Name</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" id="age" name="age" min="1" max="100" required>
                    </div>
                    <div class="form-group">
                        <label for="course">Course</label>
                        <input type="text" id="course" name="course" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="grade">Grade</label>
                        <select id="grade" name="grade" required>
                            <option value="">Select Grade</option>
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="D">D</option>
                            <option value="F">F</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="phone">Phone</label>
                        <input type="tel" id="phone" name="phone" required>
                    </div>
                </div>
                <button type="submit">Add Student</button>
            </form>
        </div>

        <div class="card">
            <h2 style="margin-bottom: 20px; color: #333;">📋 Student List</h2>
            {% if students %}
            <table class="students-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Age</th>
                        <th>Course</th>
                        <th>Grade</th>
                        <th>Phone</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student.id }}</td>
                        <td>{{ student.name }}</td>
                        <td>{{ student.email }}</td>
                        <td>{{ student.age }}</td>
                        <td>{{ student.course }}</td>
                        <td><strong>{{ student.grade }}</strong></td>
                        <td>{{ student.phone }}</td>
                        <td>
                            <button class="action-btn edit-btn" onclick="editStudent({{ student.id }})">Edit</button>
                            <button class="action-btn delete-btn" onclick="deleteStudent({{ student.id }})">Delete</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <h3>No students yet</h3>
                <p>Add your first student using the form above!</p>
            </div>
            {% endif %}
        </div>
    </div>

    <div id="editModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>✏️ Edit Student</h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <form id="editForm" method="POST">
                <input type="hidden" id="edit_id" name="id">
                <div class="form-group">
                    <label for="edit_name">Full Name</label>
                    <input type="text" id="edit_name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="edit_email">Email</label>
                    <input type="email" id="edit_email" name="email" required>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="edit_age">Age</label>
                        <input type="number" id="edit_age" name="age" min="1" max="100" required>
                    </div>
                    <div class="form-group">
                        <label for="edit_course">Course</label>
                        <input type="text" id="edit_course" name="course" required>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="edit_grade">Grade</label>
                        <select id="edit_grade" name="grade" required>
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="D">D</option>
                            <option value="F">F</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="edit_phone">Phone</label>
                        <input type="tel" id="edit_phone" name="phone" required>
                    </div>
                </div>
                <button type="submit">Update Student</button>
            </form>
        </div>
    </div>

    <script>
        function editStudent(id) {
            fetch(`/get/${id}`)
                .then(response => response.json())
                .then(student => {
                    document.getElementById('edit_id').value = student.id;
                    document.getElementById('edit_name').value = student.name;
                    document.getElementById('edit_email').value = student.email;
                    document.getElementById('edit_age').value = student.age;
                    document.getElementById('edit_course').value = student.course;
                    document.getElementById('edit_grade').value = student.grade;
                    document.getElementById('edit_phone').value = student.phone;
                    document.getElementById('editForm').action = `/edit/${id}`;
                    document.getElementById('editModal').style.display = 'block';
                });
        }

        function deleteStudent(id) {
            if (confirm('Are you sure you want to delete this student?')) {
                window.location.href = `/delete/${id}`;
            }
        }

        function closeModal() {
            document.getElementById('editModal').style.display = 'none';
        }

        window.onclick = function(event) {
            const modal = document.getElementById('editModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    students = load_students()
    courses = list(set([s['course'] for s in students])) if students else []
    return render_template_string(HTML_TEMPLATE, students=students, courses=courses)

@app.route('/add', methods=['POST'])
def add_student():
    students = load_students()
    new_id = max([s['id'] for s in students], default=0) + 1
    
    student = {
        'id': new_id,
        'name': request.form['name'],
        'email': request.form['email'],
        'age': int(request.form['age']),
        'course': request.form['course'],
        'grade': request.form['grade'],
        'phone': request.form['phone']
    }
    
    students.append(student)
    save_students(students)
    return redirect(url_for('index'))

@app.route('/get/<int:student_id>')
def get_student(student_id):
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    return jsonify(student) if student else jsonify({'error': 'Not found'}), 404

@app.route('/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if student:
        student['name'] = request.form['name']
        student['email'] = request.form['email']
        student['age'] = int(request.form['age'])
        student['course'] = request.form['course']
        student['grade'] = request.form['grade']
        student['phone'] = request.form['phone']
        save_students(students)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    students = load_students()
    students = [s for s in students if s['id'] != student_id]
    save_students(students)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)