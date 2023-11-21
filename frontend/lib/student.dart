class Student {
  final String ra;
  final String name;
  final String courseId;  

  Student({required this.ra, required this.name, required this.courseId});

  // Método para converter o objeto em um mapa, que pode ser facilmente convertido em JSON
  Map<String, dynamic> toJson() => {
    'ra': ra,
    'name': name,
    'course_id': courseId
  };

  // Método estático para criar um objeto Student a partir de um mapa (útil para desserialização)
  static Student fromJson(Map<String, dynamic> json) => Student(
    ra: json['ra'],
    name: json['name'],
    courseId: json['course_id'],
  );
}