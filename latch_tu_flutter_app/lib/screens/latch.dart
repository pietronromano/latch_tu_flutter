import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:latch_tu_flutter_app/globals.dart' as globals;
import 'package:shared_preferences/shared_preferences.dart';
//import 'package:qr_code_vision/qr_code_vision.dart';

class LatchScreen extends StatefulWidget {
  const LatchScreen({super.key});

  @override
  State<LatchScreen> createState() {
    return _LatchScreenState();
  }
}

class _LatchScreenState extends State<LatchScreen> {
  final _formKey = GlobalKey<FormState>();
  var _pairingCode = '';
  var _results = '';
  var _accountId = '';
  var _selectedCategory = "Pair";
  var _isSending = false;
  Uint8List _decodedBytes = Uint8List(1);
  var categories = ['Pair', 'Unpair', 'Status', 'Lock', 'Unlock', 'OTP'];

  void _callAPI() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      setState(() {
        _isSending = true;
        _accountId = globals.accountId;
      });

      final prefs = await SharedPreferences.getInstance();
      _decodedBytes = Uint8List(1); //reset

      String action = _selectedCategory.toLowerCase();
      String query = action;
      switch (action) {
        case 'pair':
          query = '$query/$_pairingCode';
          break;
        case 'otp':
          query = 'totp/create/${globals.accountId}';
          break;
        default:
          query = '$query/${globals.accountId}';
          break;
      }

      final url = Uri.https(globals.apiURL, 'latch/$query');
      final response = await http.get(
        url,
        headers: {
          'Content-Type': 'application/json',
          globals.apiKeyHeader: globals.apiKey
        },
      );
      if (response.body.contains('Error') ||
          response.body.contains('Not Found')) {
        _results = response.body;
        setState(() {
          _isSending = false;
        });
        return;
      }
      final Map<String, dynamic> resData = json.decode(response.body);
      switch (action) {
        case 'pair':
          _accountId = resData['account_id'];
          globals.accountId = _accountId;
          //Save state first to get the values from the form
          prefs.setString('account_id', globals.accountId);
          _results = 'Paired';
          break;
        case 'unpair':
          if (resData['result'] == '') {
            _results = 'Unpaired';
          } else {
            _results = resData.toString();
          }
          globals.accountId = '';
          _accountId = '';
          prefs.setString('account_id', globals.accountId);
          break;
        case 'status':
          if (resData['status'].toString().contains('status: on')) {
            _results = 'Latch On';
          } else {
            _results = 'Latch Off';
          }
          break;
        case 'history':
          _results = resData['result']['history'][0].toString();

          break;
        case 'lock':
          if (resData['result'] == '') {
            _results = 'Locked';
          } else {
            _results = resData.toString();
          }
          break;
        case 'unlock':
          if (resData['result'] == '') {
            _results = 'Unlocked';
          } else {
            _results = resData.toString();
          }
          break;
        case 'otp':
          String imageData = resData['result']['qr'];
          imageData = imageData.substring("data:image/png;base64,".length);
          final decoder = base64.decoder;
          _decodedBytes = decoder.convert(imageData);
          _results = "Use this QR for your One Time Password (OTP):";

          break;
        default:
          _results = resData.toString();
          break;
      }
      setState(() {
        _isSending = false;
      });
    }
  }

/*
  NOT USED - library gave byte format error
  String? decodeQr(Uint8List byteData) {
    final qrCode = QrCode();
    qrCode.scanRgbaBytes(byteData, 50, 50);
    String? decoded = '';

    if (qrCode.content != null) {
      if (qrCode.content?.text != null) {
        return qrCode.content?.text;
      }
    } else {
      return decoded;
    }
  }
*/
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Configure tu Latch...',
          style: TextStyle(fontSize: 18),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: const InputDecoration(
                  label: Text('Pairing Code'),
                ),
                onSaved: (value) {
                  _pairingCode = value!;
                },
              ),
              TextFormField(
                decoration: const InputDecoration(
                  label: Text('Account Id'),
                ),
                //onSaved: (value) {
                //  value = globals.accountId;
                //},
                initialValue: globals.accountId,
              ),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: DropdownButtonFormField(
                      value: _selectedCategory,
                      decoration: const InputDecoration(
                        label: Text('Latch Action'),
                      ),
                      items: [
                        for (final category in categories)
                          DropdownMenuItem(
                            value: category,
                            child: Row(
                              children: [
                                Text(category),
                              ],
                            ),
                          ),
                      ],
                      onChanged: (value) {
                        setState(() {
                          _selectedCategory = value!;
                        });
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  ElevatedButton(
                    onPressed: _isSending ? null : _callAPI,
                    child: _isSending
                        ? const SizedBox(
                            height: 16,
                            width: 16,
                            child: CircularProgressIndicator(),
                          )
                        : const Text('Execute Action'),
                  )
                ],
              ),
              TextFormField(
                decoration: const InputDecoration(
                  label: Text('Results'),
                ),
                enabled: true,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.start, children: [
                Text(
                  _results,
                ),
              ]),
              Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  spacing: 20,
                  children: [
                    Padding(
                        padding: const EdgeInsets.all(20),
                        child: (_decodedBytes.length > 1)
                            ? Image.memory(
                                _decodedBytes,
                                width: 200,
                                height: 200,
                              )
                            : const Text('')),
                  ]),
            ],
          ),
        ),
      ),
    );
  }
}
