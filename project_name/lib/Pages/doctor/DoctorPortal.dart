import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:project_name/Pages/features/AppointmentView.dart';
import 'package:project_name/routes.dart';

class DoctorPortal extends StatefulWidget {
  final String? token;
  final int doctorId;
  const DoctorPortal({super.key, required this.token, required this.doctorId});

  @override
  State<DoctorPortal> createState() => _DoctorPortalState();
}

class _DoctorPortalState extends State<DoctorPortal> {
  List<dynamic> Datas = [];

  @override
  void initState() {
    super.initState();
    getAppointment();
  }



  Future<void> getAppointment() async {

    final url = Uri.parse(routes.doctorAppointment(widget.doctorId, widget.token!));
    final response = await http.get(url);
    if (response.statusCode == 200){
      final data = json.decode(response.body);
      Datas = data;
    }
    else{
      print(response.statusCode);
      print('Error: Failed to get data from the server.');
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text(
          'Doctor Portal',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 32.0)
        ),
        centerTitle: true,
      ),
      body:Container(
      child:  FutureBuilder<void>(
        future: getAppointment(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('Error: ${snapshot.error}'),
            );
          }
          else{
            return ListView.builder(
                  itemCount: Datas.length,
                  itemBuilder: (context, index) {
                    var Data = Datas[index];
              return  AppointmentView(data:Data);
            },
          );
          }
        }
      )
    )
    );
  }
}