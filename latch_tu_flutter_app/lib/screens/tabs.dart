import 'package:flutter/material.dart';
import 'package:latch_tu_flutter_app/widgets/access_list.dart';
import 'package:latch_tu_flutter_app/screens/latch.dart';
import 'package:latch_tu_flutter_app/screens/webhooks.dart';

class TabsScreen extends StatefulWidget {
  const TabsScreen({super.key});

  @override
  State<TabsScreen> createState() {
    return _TabsScreenState();
  }
}

class _TabsScreenState extends State<TabsScreen> {
  int _selectedPageIndex = 0;

  void _selectPage(int index) {
    setState(() {
      _selectedPageIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    Widget activePage = const AccessList();

    switch (_selectedPageIndex) {
      case 0:
        activePage = const LatchScreen();
        break;
      case 1:
        activePage = const AccessList();
        break;
      case 2:
        activePage = const WebHookScreen();
        break;
      default:
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Latch tu Flutter'),
      ),
      body: activePage,
      bottomNavigationBar: BottomNavigationBar(onTap: _selectPage, items: [
        BottomNavigationBarItem(
            icon: Image.asset('assets/images/tu-latch.png',
                height: 40, width: 40),
            label: 'tu Latch'),
        BottomNavigationBarItem(
            icon:
                Image.asset('assets/images/access.png', height: 40, width: 40),
            label: 'Access'),
        BottomNavigationBarItem(
            icon:
                Image.asset('assets/images/webhook.png', height: 40, width: 40),
            label: 'Webhook'),
      ]),
    );
  }
}
