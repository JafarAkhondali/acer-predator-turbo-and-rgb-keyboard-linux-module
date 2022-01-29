use crate::{Client, Clients};
use crate::mods::payload::Payload;
use crate::mods::static_payload::create_static_payload;
use crate::mods::last_mode::last_mode;
use futures::{FutureExt, StreamExt};
use tokio::sync::mpsc;
use tokio_stream::wrappers::UnboundedReceiverStream;
use uuid::Uuid;
use warp::ws::{Message, WebSocket};

use std::{fs, fs::File, io::prelude::*, env};
use toml;
use serde_derive::Deserialize;

#[derive(Deserialize)]
struct General {
    restore_conf: String,
}

pub async fn client_connection(ws: WebSocket, clients: Clients) {
    let mut confile = File::open(format!("{}/.config/keybrgbctl.cfg", env::var("HOME").unwrap())).expect("Unable to open the Config file, does ~/.config/keybrgbctl.cfg exit?");
    let mut config = String::new();
    let conftostring = fs::read_to_string(format!("{}/.config/keybrgbctl.cfg", env::var("HOME").unwrap())).expect("unable to open config file!");
    let defaultconfig = format!(r#"
        websocket_ip = "127.0.0.1"
        websocket_port = "8080"
        restore_conf = "{}/.cache/lastPayload"
    "#, env::var("HOME").unwrap());
    let mut _configfile: General = toml::from_str(&defaultconfig).unwrap();
    match conftostring.as_str() {
        "" => {
            _configfile = toml::from_str(&defaultconfig).unwrap();
        }
        _ => {
            confile.read_to_string(&mut config).expect("Unable to read the Config file");
            _configfile = toml::from_str(&config).unwrap();
        }
    }
    println!("establishing client connection... {:?}", ws);

    let (client_ws_sender, mut client_ws_rcv) = ws.split();
    let (client_sender, client_rcv) = mpsc::unbounded_channel();

    let client_rcv = UnboundedReceiverStream::new(client_rcv);

    tokio::task::spawn(client_rcv.forward(client_ws_sender).map(|result| {
        if let Err(e) = result {
            println!("error sending websocket msg: {}", e);
        }
    }));

    let uuid = Uuid::new_v4().simple().to_string();

    let new_client = Client {
        client_id: uuid.clone(),
        sender: Some(client_sender),
    };

    clients.lock().await.insert(uuid.clone(), new_client);
    while let Some(result) = client_ws_rcv.next().await {
        let msg = match result {
            Ok(msg) => msg,
            Err(e) => {
                println!("error receiving message for id {}): {}", uuid.clone(), e);
                break;
            }
        };
        client_msg(&uuid, msg, _configfile.restore_conf.as_str(), &clients).await;
    }
    clients.lock().await.remove(&uuid);
    println!("{} disconnected", uuid);
}

async fn client_msg(client_id: &str, msg: Message, restore_conf: &str, clients: &Clients) {
    println!("received message from {}: {:?}", client_id, msg);

    let message = match msg.to_str() {
        Ok(v) => v,
        Err(_) => return,
    };

    let data = message.split(",").collect::<Vec<&str>>();
    println!("data: {:?}", data);
    let client = data[0];
    let mode = data[1];
    let speed = data[2].parse::<u8>().unwrap();
    let brightness = data[3].parse::<u8>().unwrap();
    let direction = data[4];
    let cvec = data[5].to_string().chars().collect::<Vec<char>>();
    let mut color = String::new();
    if client == "phone" {
        for i in 2..cvec.len() {
            color.push(cvec[i]);
        }
    } else {
        color = data[5].to_string();
    }
    if mode == "static" {
        println!("Creating static payload...");
        let payload = Payload::new(
            mode.to_string(),
            speed,
            brightness,
            direction.to_string(),
            color.to_string().replace("\n", "").replace("#", "").replace(")", "").replace("(", ""),
            restore_conf.to_string(),
        );
        let code = create_static_payload(payload, restore_conf.to_string());
        match code {
            Ok(_) => {
                println!("Success!");
            },
            Err(e) => {
                println!("Error: {}", e);
            }
        }
    } else if mode == "get" {
        let last_mode: Payload = last_mode();
        let send_back: String;
        match data[4] {
            "mode" => {
                send_back = format!("{}", last_mode.get_mode());
            },
            "speed" => {
                send_back = format!("{}", last_mode.get_speed());
            },
            "brightness" => {
                send_back = format!("{}", last_mode.get_brightness());
            },
            "direction" => {
                send_back = format!("{}", last_mode.get_direction());
            },
            "color" => {
                send_back = format!("{}", last_mode.get_color());
            },
            _ => {
                send_back = "error".to_string();
            }
        }
        let locked = clients.lock().await;
        match locked.get(client_id) {
            Some(v) => {
                if let Some(sender) = &v.sender {
                    let _ = sender.send(Ok(Message::text(format!("{}", send_back).as_str())));
                }
            }
            None => return,
        }
    } else {
        println!("Creating dynamic payload...");
        let payload = Payload::new(
            mode.to_string(),
            speed,
            brightness,
            direction.to_string(),
            color.to_string().replace("\n", "").replace("#", "").replace(")", "").replace("(", ""),
            restore_conf.to_string(),
        );
        let code = payload.send_payload();
        match code {
            Ok(_) => {
                println!("Success!");
            },
            Err(e) => {
                println!("Error: {}", e);
            }
        }
    }
}