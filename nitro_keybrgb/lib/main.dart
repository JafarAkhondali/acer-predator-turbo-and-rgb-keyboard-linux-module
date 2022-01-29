import 'package:flutter/material.dart';
import 'package:flutter_hsvcolor_picker/flutter_hsvcolor_picker.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:select_form_field/select_form_field.dart';

void main() => runApp(
      MaterialApp(
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
    channel.sink.add("phone,$mode,$speed,$bright,$dir,$col");
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
      'icon': Icon(Icons.lightbulb_outline),
    },
    {
      'value': 'breath',
      'label': 'Breath',
      'icon': Icon(Icons.lightbulb_outline),
    },
    {
      'value': 'neon',
      'label': 'Neon',
      'icon': Icon(Icons.change_circle),
    },
    {
      'value': 'wave',
      'label': 'Wave',
      'icon': Icon(Icons.waves),
    },
    {
      'value': 'shifting',
      'label': 'Shifting',
      'icon': Icon(Icons.play_arrow),
    },
    {
      'value': 'zoom',
      'label': 'Zoom',
      'icon': Icon(Icons.zoom_out_map),
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        title: Text('Keybrgb'),
        centerTitle: true,
        backgroundColor: colorCurr,
        actions: <Widget>[
          IconButton(
            icon: Icon(
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
        child: Icon(Icons.send),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            SelectFormField(
              type: SelectFormFieldType.dropdown, // or can be dialog
              cursorColor: colorCurr,
              changeIcon: true,
              initialValue: 'static',
              icon: Icon(Icons.light),
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
            SizedBox(height: 40),
            Visibility(
              visible: colorVisible,
              child: ColorPicker(
                initialPicker: Picker.wheel,
                color: Colors.purpleAccent,
                onChanged: (color) {
                  setColor = color.withAlpha(255).toString().substring(8);
                  setState(() {
                    colorCurr = color;
                  });
                },
              ),
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
            SizedBox(height: 20),
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
                    icon: Icon(Icons.arrow_back),
                    label: Text('Left'),
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
                    icon: Icon(Icons.arrow_forward),
                    label: Text('Right'),
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
