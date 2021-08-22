//! Refer to [Boosery & Hawkes](https://www.boosey.com/downloads/BH_StandardAbbreviations_New.pdf)
//! for conventions for name abbreviations
//! 


use std::path::{PathBuf, Path};


#[derive(Clone)]
pub struct Part {
    pub path: PathBuf,
    pub part_raw: String,
    pub n_copies: u32,
}

impl Part {
    pub fn new<P: Into<PathBuf>>(path: P, abbreviations: &json::JsonValue) -> Part {

        let path: PathBuf = path.into();
        let filename = path
            .file_stem().unwrap()
            .to_str().unwrap();
        let mut part_raw = filename
            .split(" - ")
            .last().unwrap()
            .to_string();
        eprintln!("'{:?}' from {:?}", part_raw, filename);
        // TODO: regex is slow, needs optimizing
        for entry in abbreviations.members() {
            
            let re = fancy_regex::Regex::new(&format!(r"(?i)(?<![a-zA-ZæøåÆØÅ])({})s?(?![a-zA-ZæøåÆØÅ])", entry["abbr"].as_str().unwrap())).unwrap();
            
            let res = re
                .replace_all(
                    &part_raw,
                    entry["no"]     // TODO: language selection + fallback on missing entries
                        .as_str()
                        .unwrap()
                );
            if res != part_raw {
                eprintln!("'{}' changed to '{}'", part_raw, res);
                part_raw = res.into_owned();
            }
        }
        eprintln!("After replace: {}", part_raw);
        Part {
            path: path.clone(),
            part_raw: String::from(part_raw),
            n_copies: 1,
        }
    }
}