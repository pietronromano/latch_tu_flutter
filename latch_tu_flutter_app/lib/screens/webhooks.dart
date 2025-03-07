import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:latch_tu_flutter_app/globals.dart' as globals;

class WebHookScreen extends StatefulWidget {
  const WebHookScreen({super.key});

  @override
  State<WebHookScreen> createState() => _WebHookScreenState();
}

class _WebHookScreenState extends State<WebHookScreen> {
  final TextEditingController _controller = TextEditingController();

  final WebSocketChannel _channel =
      WebSocketChannel.connect(Uri.parse('wss://${globals.wsURL}/ws'));
  //WebSocketChannel.connect(Uri.parse('ws://localhost:8001/ws'));
  // PUBLIC TESTER:  WebSocketChannel.connect(Uri.parse('wss://echo.websocket.events'));

  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      try {
        _channel.sink.add(_controller.text);
      } catch (e, s) {
        print(e);
        print(s);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Webhooks')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Form(
              child: TextFormField(
                controller: _controller,
                decoration: const InputDecoration(labelText: 'Message'),
              ),
            ),
            const SizedBox(height: 24),
            StreamBuilder(
              stream: _channel.stream,
              builder: (context, snapshot) {
                return Text(snapshot.hasData ? '${snapshot.data}' : '');
              },
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _sendMessage,
        tooltip: 'Send message',
        child: const Icon(Icons.send),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }

  @override
  void dispose() {
    try {
      _channel.sink.close();
    } catch (e, s) {
      print(e);
      print(s);
    }
    _controller.dispose();
    super.dispose();
  }
}
