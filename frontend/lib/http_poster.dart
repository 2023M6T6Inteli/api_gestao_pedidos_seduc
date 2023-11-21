import 'package:http/http.dart' as http;
import 'dart:convert';
import 'student.dart';

class HttpPoster {
  Future<void> enrollStudent(Student student) async {

    var url = Uri.parse('http://127.0.0.1:5000/enroll_student');
    var encoded = json.encode(student.toJson());
    var response = await http.post(url, body: encoded);

    if (response.statusCode == 200) {
      print("Sucesso");
    } else {
      print("Erro");
    }
  }
}