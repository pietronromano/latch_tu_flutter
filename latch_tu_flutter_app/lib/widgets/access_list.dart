import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:latch_tu_flutter_app/data/buildings.dart';
import 'package:latch_tu_flutter_app/globals.dart' as globals;

import 'package:latch_tu_flutter_app/models/access_item.dart';
import 'package:latch_tu_flutter_app/widgets/new_item.dart';

class AccessList extends StatefulWidget {
  const AccessList({super.key});

  @override
  State<AccessList> createState() => _AccessListState();
}

class _AccessListState extends State<AccessList> {
  List<AccessItem> _accessItems = [];
  var _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadItems();
  }

  void _loadItems() async {
    final url = Uri.https(globals.firebaseURL, 'access-list.json');

    try {
      final response = await http.get(url);

      if (response.statusCode >= 400) {
        setState(() {
          _error = 'Failed to fetch data. Please try again later.';
        });
      }

      if (response.body == 'null') {
        setState(() {
          _isLoading = false;
        });
        return;
      }

      final Map<String, dynamic> listData = json.decode(response.body);
      final List<AccessItem> loadedItems = [];
      for (final item in listData.entries) {
        final building = buildings.entries
            .firstWhere(
                (catItem) => catItem.value.title == item.value['building'])
            .value;
        loadedItems.add(
          AccessItem(
              id: item.key,
              name: item.value['name'],
              hours: item.value['hours'],
              building: building,
              accountId: globals.accountId),
        );
      }
      setState(() {
        _accessItems = loadedItems;
        _isLoading = false;
      });
    } catch (error) {
      setState(() {
        _error = 'Something went wrong! Please try again later.';
      });
    }
  }

  void _addItem() async {
    final newItem = await Navigator.of(context).push<AccessItem>(
      MaterialPageRoute(
        builder: (ctx) => const NewItem(),
      ),
    );

    if (newItem == null) {
      return;
    }

    setState(() {
      _accessItems.add(newItem);
    });
  }

  void _removeItem(AccessItem item) async {
    final index = _accessItems.indexOf(item);
    setState(() {
      _accessItems.remove(item);
    });

    final url = Uri.https(globals.firebaseURL, 'access-list/${item.id}.json');

    final response = await http.delete(url);

    if (response.statusCode >= 400) {
      setState(() {
        _accessItems.insert(index, item);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    Widget content = const Center(child: Text('No items added yet.'));

    if (_isLoading) {
      content = const Center(child: CircularProgressIndicator());
    }

    if (globals.accountId == '') {
      content = const Center(
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Text(
            'Please pair with Latch before registering Accesses',
            style: TextStyle(
              color: Colors.red,
              fontSize: 18,
            ),
          ),
        ),
      );
    } else {
      if (_accessItems.isNotEmpty) {
        content = ListView.builder(
          itemCount: _accessItems.length,
          itemBuilder: (ctx, index) => Dismissible(
            onDismissed: (direction) {
              _removeItem(_accessItems[index]);
            },
            key: ValueKey(_accessItems[index].id),
            child: ListTile(
              title: Text(_accessItems[index].name),
              leading: Container(
                width: 24,
                height: 24,
                color: _accessItems[index].building.color,
              ),
              trailing: Text(
                _accessItems[index].hours.toString(),
              ),
            ),
          ),
        );
      }
    }

    if (_error != null) {
      content = Center(child: Text(_error!));
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Building Accesses'),
        actions: [
          IconButton(
            onPressed: _addItem,
            icon: const Icon(Icons.add),
          ),
        ],
      ),
      body: content,
    );
  }
}
