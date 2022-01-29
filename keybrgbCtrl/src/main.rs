mod mods;
use clap::{Arg, App};
use mods::payload::Payload;
use std::{collections::HashMap, convert::Infallible, sync::Arc, fs, fs::File, io::prelude::*, env};
use tokio::sync::{mpsc, Mutex};
use warp::{ws::Message, Filter, Rejection};
use mods::static_payload::create_static_payload;
use toml;
use serde_derive::Deserialize;

#[derive(Deserialize)]
struct General {
    websocket_ip: String,
    websocket_port: String,
    restore_conf: String,
}


#[derive(Debug, Clone)]
pub struct Client {
    pub client_id: String,
    pub sender: Option<mpsc::UnboundedSender<std::result::Result<Message, warp::Error>>>,
}

type Clients = Arc<Mutex<HashMap<String, Client>>>;
type Result<T> = std::result::Result<T, Rejection>;

#[tokio::main]
pub async fn start_websocket(ip: String, port: String, _restore_conf: String) {
    let clients: Clients = Arc::new(Mutex::new(HashMap::new()));
    let ip_split = ip.split(".").collect::<Vec<&str>>();
    let ip: (u8, u8, u8, u8) = (
        ip_split[0].parse::<u8>().unwrap(),
        ip_split[1].parse::<u8>().unwrap(),
        ip_split[2].parse::<u8>().unwrap(),
        ip_split[3].parse::<u8>().unwrap(),
    );
    println!("Configuring websocket route");
    let ws_route = warp::path("ws")
        .and(warp::ws())
        .and(with_clients(clients.clone()))
        .and_then(mods::handlers::ws_handler);

    let routes = ws_route.with(warp::cors().allow_any_origin());
    println!("Starting server");
    warp::serve(routes).run(([ip.0, ip.1, ip.2, ip.3], port.as_str().parse::<u16>().unwrap())).await;
}

fn with_clients(clients: Clients) -> impl Filter<Extract = (Clients,), Error = Infallible> + Clone {
    warp::any().map(move || clients.clone())
}


fn main() {
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
    
    let matches = App::new("keybrgbCtrl") // set up all the args
                            .version("0.1.0")
                            .author("amy <axtlos@tar.black>")
                            .about("Control your keyboard backlight")
                            .arg(Arg::with_name("websocket")
                                .short("ws")
                                .long("websocket")
                                .help("Start websocket server")
                                .takes_value(false))
                            .arg(Arg::with_name("mode")
                                .short("m")
                                .long("mode")
                                .value_name("MODE")
                                .help("Set the mode of the keyboard")
                                .takes_value(true)
                                .possible_values(&["static", "breath", "neon", "wave", "shifting", "zoom"])
                                .required(false))
                            .arg(Arg::with_name("speed")
                                .short("s")
                                .long("speed")
                                .value_name("SPEED")
                                .help("Set the speed of the keyboard")
                                .min_values(0)
                                .max_values(9)
                                .takes_value(true))
                            .arg(Arg::with_name("brightness")
                                .short("b")
                                .long("brightness")
                                .value_name("BRIGHTNESS")
                                .help("Set the brightness of the keyboard")
                                .min_values(0)
                                .max_values(100)
                                .takes_value(true))
                            .arg(Arg::with_name("direction")
                                .short("d")
                                .long("direction")
                                .value_name("DIRECTION")
                                .help("Set the direction of the keyboard")
                                .takes_value(true)
                                .possible_values(&["left", "right"]))
                            .arg(Arg::with_name("color")
                                .short("c")
                                .long("color")
                                .value_name("COLOR")
                                .help("Set the color of the keyboard")
                                .takes_value(true))
                            .get_matches();

    let mode = matches.value_of("mode").unwrap_or("static");
    let speed = matches.value_of("speed").unwrap_or("3");
    let brightness = matches.value_of("brightness").unwrap_or("100");
    let direction = matches.value_of("direction").unwrap_or("left");
    let color = matches.value_of("color").unwrap_or("#ffffff");
    let payload = Payload::new(
        mode.to_string(),
        speed.parse::<u8>().unwrap(),
        brightness.parse::<u8>().unwrap(),
        direction.to_string(),
        color.to_string(),
        _configfile.restore_conf.to_string(),
    );
    println!("{:?}", matches.occurrences_of("websocket"));

    if matches.occurrences_of("websocket") > 0 {
        start_websocket(_configfile.websocket_ip.clone(), _configfile.websocket_port.clone(), _configfile.restore_conf.to_string());
    } else {
        if mode == "static" {
            println!("Creating static payload...");
            let code = create_static_payload(payload, _configfile.restore_conf.to_string());
            match code {
                Ok(_) => {
                    println!("Success!");
                },
                Err(e) => {
                    println!("Error: {}", e);
                }
            }
        } else {
            println!("Creating dynamic payload...");
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
}
