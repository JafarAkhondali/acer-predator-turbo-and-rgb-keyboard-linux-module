use crate::{Client, Clients};
use crate::payload::Payload;
use crate::static_payload::create_static_payload;
use futures::{FutureExt, StreamExt};
use tokio::sync::mpsc;
use tokio_stream::wrappers::UnboundedReceiverStream;
use uuid::Uuid;
use warp::ws::{Message, WebSocket};

pub async fn client_connection(ws: WebSocket, clients: Clients) {
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
        client_msg(&uuid, msg).await;
    }

    clients.lock().await.remove(&uuid);
    println!("{} disconnected", uuid);
}

async fn client_msg(client_id: &str, msg: Message) {
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
    } else if client == "desktop" {
        color = data[5].to_string();
    }


    let payload = Payload::new(
        mode.to_string(),
        speed,
        brightness,
        direction.to_string(),
        color.to_string().replace("\n", "").replace("#", "").replace(")", "").replace("(", ""),
    );
    println!("payload color: {:?}", payload.get_color());
    println!("payload rgb: {:?}", payload.get_rgb());
    if mode == "static" {
        //println!("Creating static payload...");
        let code = create_static_payload(payload);
        match code {
            Ok(_) => {
                println!("Success!");
            },
            Err(e) => {
                println!("Error: {}", e);
            }
        }
    } else {
        //println!("Creating dynamic payload...");
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