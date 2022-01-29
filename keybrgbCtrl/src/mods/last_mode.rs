use std::{fs, fs::File, io::prelude::*, env};
use toml;
use serde_derive::Deserialize;
use crate::mods::payload::Payload;

#[derive(Deserialize)]
struct General {
    restore_conf: String,
}

pub fn last_mode () -> Payload {
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

    let mut last_payload = fs::read_to_string(_configfile.restore_conf.as_str()).expect("Unable to read the lastPayload file");
    last_payload = last_payload.replace("\n", "").replace("[", "").replace("]", "").replace(" ", "");
    let last_payload: Vec<&str> = last_payload.split(",").collect();

    let mode: &str;
    if last_payload[15] == "0:STATIC" {
        mode = "static";
    } else {
        match last_payload[0] {
            "1" => mode = "breath",
            "2" => mode = "neon",
            "3" => mode = "shifting",
            "4" => mode = "zoom",
            _ => mode = "static",
        }
    }
    let speed = last_payload[1].parse::<u8>().unwrap();
    let brightness = last_payload[2].parse::<u8>().unwrap();
    let direction = if last_payload[4] == "0" { "left" } else { "right" };
    let c_r = last_payload[5].parse::<u8>().unwrap();
    let c_g = last_payload[6].parse::<u8>().unwrap();
    let c_b = last_payload[7].parse::<u8>().unwrap();
    let color = String::from(format!("{:02x}{:02x}{:02x}", c_r, c_g, c_b));
    let payload = Payload::new(String::from(mode), speed, brightness, String::from(direction), color, _configfile.restore_conf.clone());
    payload
}