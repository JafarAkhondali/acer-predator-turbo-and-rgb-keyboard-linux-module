import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:select_form_field/select_form_field.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';

void main() => runApp(
      const MaterialApp(
        home: Keyrgb(),
      ),
    );

class Keyrgb extends StatefulWidget {
  const Keyrgb({Key? key}) : super(key: key);

  @override
  _KeyrgbState createState() => _KeyrgbState();
}

class _KeyrgbState extends State<Keyrgb> {
  WebSocketChannel channel = WebSocketChannel.connect(
    Uri.parse('ws://127.0.0.1:8080/ws'),
  );

  WebSocketChannel connect() {
    WebSocketChannel channel =
        WebSocketChannel.connect(Uri.parse('ws://127.0.0.1:8080/ws'));
    return channel;
  }

  submit(WebSocketChannel channel, String col, String bright, String speed,
      String mode, String dir) async {
    channel.sink.add("desktop,$mode,$speed,$bright,$dir,$col");
  }

  updateButton(String dir, String button) {
    if (dir == "left" && button == "left") {
      return Colors.grey[400];
    } else if (dir == "right" && button == "right") {
      return Colors.grey[400];
    } else if (dir == "left" && button == "right") {
      return colorCurr;
    } else if (dir == "right" && button == "left") {
      return colorCurr;
    } else {
      return colorCurr;
    }
  }

  bool colorVisible = true;
  bool speedVisible = false;
  bool dirVisible = false;
  double speed = 3;
  double bright = 100;
  String setColor = 'e040fb';
  String mode = "static";
  String dir = "left";
  Color colorCurr = Colors.purpleAccent;

  final List<Map<String, dynamic>> _items = [
    {
      'value': 'static',
      'label': 'Static',
      'icon': const Icon(Icons.lightbulb_outline),
    },
    {
      'value': 'breath',
      'label': 'Breath',
      'icon': const Icon(Icons.lightbulb_outline),
    },
    {
      'value': 'neon',
      'label': 'Neon',
      'icon': const Icon(Icons.change_circle),
    },
    {
      'value': 'wave',
      'label': 'Wave',
      'icon': const Icon(Icons.waves),
    },
    {
      'value': 'shifting',
      'label': 'Shifting',
      'icon': const Icon(Icons.play_arrow),
    },
    {
      'value': 'zoom',
      'label': 'Zoom',
      'icon': const Icon(Icons.zoom_out_map),
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        title: const Text('Keybrgb'),
        centerTitle: true,
        backgroundColor: colorCurr,
        actions: <Widget>[
          IconButton(
            icon: const Icon(
              Icons.wifi,
              color: Colors.white,
            ),
            onPressed: () {
              setState(() {
                channel = connect();
              });
            },
          )
        ],
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: colorCurr,
        onPressed: () {
          submit(channel, setColor, bright.round().toString(),
              speed.round().toString(), mode, dir);
        },
        child: const Icon(Icons.send),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SelectFormField(
              type: SelectFormFieldType.dropdown, // or can be dialog
              cursorColor: colorCurr,
              changeIcon: true,
              initialValue: 'static',
              icon: const Icon(Icons.light),
              labelText: 'Mode',
              items: _items,
              onChanged: (val) {
                if (val == "static") {
                  setState(() {
                    colorVisible = true;
                    speedVisible = false;
                    dirVisible = false;
                  });
                } else if (val == "breath") {
                  setState(() {
                    colorVisible = true;
                    speedVisible = true;
                    dirVisible = false;
                  });
                } else if (val == "neon") {
                  setState(() {
                    colorVisible = false;
                    speedVisible = true;
                    dirVisible = false;
                  });
                } else if (val == "wave") {
                  setState(() {
                    colorVisible = false;
                    speedVisible = true;
                    dirVisible = true;
                  });
                } else if (val == "shifting") {
                  setState(() {
                    colorVisible = true;
                    speedVisible = true;
                    dirVisible = true;
                  });
                } else if (val == "zoom") {
                  setState(() {
                    colorVisible = true;
                    speedVisible = true;
                    dirVisible = false;
                  });
                }
                setState(() {
                  mode = val;
                });
              },
            ),
            const SizedBox(height: 40),
            Visibility(
              visible: colorVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ColorPicker(
                    pickerColor: colorCurr,
                    onColorChanged: (color) {
                      setState(() {
                        colorCurr = color;
                        setColor = color.value.toRadixString(16).substring(2);
                      });
                    },
                  ),
                ],
              ),
              /*ColorPicker(
                initialPicker: Picker.wheel,
                color: Colors.purpleAccent,
                onChanged: (color) {
                  setColor = color.withAlpha(255).toString().substring(8);
                  setState(() {
                    colorCurr = color;
                  });
                },
              ),*/
            ),
            Slider(
              value: bright,
              max: 100,
              divisions: 100,
              thumbColor: colorCurr,
              activeColor: colorCurr,
              label: bright.round().toString(),
              onChanged: (double value) {
                setState(() {
                  bright = value;
                });
              },
            ),
            const SizedBox(height: 20),
            Visibility(
              visible: speedVisible,
              child: Slider(
                value: speed,
                max: 9,
                divisions: 9,
                thumbColor: colorCurr,
                activeColor: colorCurr,
                label: speed.round().toString(),
                onChanged: (double value) {
                  setState(() {
                    speed = value;
                  });
                },
              ),
            ),
            Visibility(
              visible: dirVisible,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  TextButton.icon(
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Left'),
                    style: TextButton.styleFrom(
                      primary: updateButton(dir, "right"),
                    ),
                    onPressed: () {
                      if (dir != "right") {
                        setState(() {
                          updateButton(dir, "right");
                          dir = "right";
                        });
                      }
                    },
                  ),
                  TextButton.icon(
                    icon: const Icon(Icons.arrow_forward),
                    label: const Text('Right'),
                    style: TextButton.styleFrom(
                      primary: updateButton(dir, "left"),
                    ),
                    onPressed: () {
                      if (dir != "left") {
                        setState(() {
                          updateButton(dir, "left");
                          dir = "left";
                        });
                      }
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
