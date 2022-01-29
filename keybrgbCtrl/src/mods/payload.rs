use std::{process,
          fs::OpenOptions,
          fs::File,
          io::Write};
use crate::mods::hexrgb::convert_hexcode_to_rgb;

static PAYLOAD_SIZE: usize = 16;
static CHARACHTER_DEVICE: &str = "/dev/acer-gkbbl-0";

pub struct Payload {
    mode: String,
    speed: u8,
    brightness: u8,
    direction: String,
    color: String,
    rgb: Vec<u8>,
    restore_conf: String
}

impl Payload { 
    pub fn new(mode: String, speed: u8, brightness: u8, direction: String, color: String, restore_conf: String) -> Payload {
        let rgb: Vec<u8> = convert_hexcode_to_rgb(color.as_str());
        Payload {
            mode,
            speed,
            brightness,
            direction,
            color,
            rgb,
            restore_conf,
        }
    }

    pub fn send_payload(&self) -> std::io::Result<()> {
        let mut _mode_payload = 1;
        match self.mode.as_str() {
            "breath" => {
                _mode_payload = 1;
            },
            "neon" => {
                _mode_payload = 2;
            },
            "wave" => {
                _mode_payload = 3;
            },
            "shifting" => {
                _mode_payload = 4;
            },
            "zoom" => {
                _mode_payload = 5;
            },
            _ => {
                println!("ERROR: mode {} is not supported", self.mode);
                process::exit(1);
            }
        }   
        let mut _direction_payload = 1;
        if self.direction == "left" {
            _direction_payload = 1;
        } else if self.direction == "right" {
            _direction_payload = 2;
        } else {
            println!("ERROR: direction {} is not supported", self.direction);
            process::exit(1);
        }

        let mut payload: Vec<u8> = Vec::new();
        payload.push(_mode_payload as u8);
        payload.push(self.speed as u8);
        payload.push(self.brightness as u8);
        if _mode_payload == 3 {
            payload.push(8);
        } else {
            payload.push(0);
        }
        payload.push(_direction_payload as u8);
        payload.push(self.rgb[0] as u8);
        payload.push(self.rgb[1] as u8);
        payload.push(self.rgb[2] as u8);
        while payload.len() != PAYLOAD_SIZE {
            payload.push(0);
        }
        let c: &[u8] = &payload;
        let mut file = OpenOptions::new().write(true).create(false).open(CHARACHTER_DEVICE)?;
        file.write(c)?;
        let path = self.restore_conf.as_str();
        let mut safe = File::create(path)?;
        let payload_as_string = format!("{:?}", payload);
        write!(safe, "{}", payload_as_string)?;
        Ok(())
    }
    pub fn get_mode(&self) -> String {
        self.mode.clone()
    }
    pub fn get_speed(&self) -> u8 {
        self.speed
    }
    pub fn get_brightness(&self) -> u8 {
        self.brightness
    }
    pub fn get_direction(&self) -> String {
        self.direction.clone()
    }
    pub fn get_color(&self) -> String {
        self.color.clone()
    }
    /*pub fn get_rgb(&self) -> Vec<u8> {
        self.rgb.clone()
    }*/
    pub fn get_safe(&self) -> String {
        self.restore_conf.clone()
    }
}