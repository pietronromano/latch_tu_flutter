import 'package:flutter/material.dart';
import 'package:latch_tu_flutter_app/screens/tabs.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:latch_tu_flutter_app/globals.dart' as globals;

Future<void> main() async {
  // Load and obtain the shared preferences for this app.
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  globals.accountId = prefs.getString('account_id') ?? '';
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Latch tu Flutter',
      theme: ThemeData.dark().copyWith(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color.fromARGB(255, 147, 229, 250),
          brightness: Brightness.dark,
          surface: const Color.fromARGB(255, 42, 51, 59),
        ),
        scaffoldBackgroundColor: const Color.fromARGB(255, 50, 58, 60),
      ),
      home: const TabsScreen(),
    );
  }
}
