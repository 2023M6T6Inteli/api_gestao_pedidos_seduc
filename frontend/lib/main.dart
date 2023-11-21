import 'package:flutter/material.dart';
import 'student.dart';
import 'http_poster.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Tela de Matrícula',
      home: EnrollmentScreen(),
    );
  }
}

class EnrollmentScreen extends StatefulWidget {
  const EnrollmentScreen({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _EnrollmentScreenState createState() => _EnrollmentScreenState();
}

class _EnrollmentScreenState extends State<EnrollmentScreen> {
  final TextEditingController _courseIdController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _raController = TextEditingController();

  @override
  void dispose() {
    _raController.dispose();
    _nameController.dispose();
    _courseIdController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tela de Matrícula'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextField(
              controller: _raController,
              decoration: const InputDecoration(
                labelText: 'RA (Registro Acadêmico)',
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Nome',
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _courseIdController,
              decoration: const InputDecoration(
                labelText: 'CourseId',
              ),
            ),
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: ()  {                
                // Cria uma instância de Student
                Student student = Student(
                  ra: _raController.text,
                  name: _nameController.text,
                  courseId: _courseIdController.text
                );
            
                final HttpPoster poster = HttpPoster();
                poster.enrollStudent(student);
              },
              child: const Text('Matricular'),
            ),
          ],
        ),
      ),
    );
  }
}