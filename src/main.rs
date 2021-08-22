//! PrintOrch
//! 
//! Future for a GUI: Tauri https://dev.to/davidedelpapa/rust-gui-introduction-a-k-a-the-state-of-rust-gui-libraries-as-of-january-2021-40gl

use native_dialog::FileDialog;

use std::fs::{self, DirEntry};

mod pdf;
mod instrument;
mod fsm;

// fn is_pdf(path: &std::path::PathBuf) -> bool {
//     path.extension()
// }

/// # The console setup
/// ```txt
/// ================================================================================
/// | Seleced directory: /home/example/Documents/Composer - Score/
/// | Selected output directory: /home/example/Documents/
/// | Merged file name: composer_score_printready.pdf
/// --------------------------------------------------------------------------------
/// | Parts         | Number of copies
/// --------------------------------------------------------------------------------
/// | fl_1          | 1
/// | Clarinet 1    | 1
/// | Violin 1      | 8
/// | Timpani       | 2
/// --------------------------------------------------------------------------------
/// Actions:
/// 1) Select input directory
/// 2) Select output directory
/// 3) Change merged file name
/// 4) Change numbers of copies
/// 5) Merge and save
/// 0) Quit
/// : 
/// ================================================================================
/// ```



fn main() {
    let abbreviations = json::parse(&std::fs::read_to_string("src/abbreviations.json").unwrap()).unwrap();
    //println!("{:?}", abbreviations);

    

    let stdin = std::io::stdin();
    let mut buf = String::new();
    // stdin.read_line(&mut buf);

    let mut state = fsm::FSM { in_dir: None, out_dir: None, out_name: String::new(), docs: Vec::new() };
    // /* Main loop */
    // loop {

    // }


    // get a path
    state.in_dir = FileDialog::new()
        .set_location("/home/andreas/dev/PrintOrch/dev_resources")
        .show_open_single_dir()
        .unwrap();

    if let Some(path) = state.in_dir.clone() {
        println!("Selected directory is {:?}", path);
        let mut files = Vec::new();
    
        let start = std::time::SystemTime::now();
        for entry in fs::read_dir(path).unwrap() {
            let entry = entry.unwrap();
            // Check extension
            if let Some(ext) = entry.path().extension() {
                if ext == "pdf" {
                    files.push(entry.path());//.push(lopdf::Document::load(entry.path()).unwrap());
                    state.docs.push(instrument::Part::new(entry.path(), &abbreviations));
                }
            }
        }
        println!("Loading parts took {:?} ms", start.elapsed().unwrap().as_millis());
        println!("{:?}", state.in_dir.unwrap().file_name());
        for part in state.docs.iter() {
            println!("{}", part.part_raw);
        }
        return;
        files.sort();

        // Load all selected files
        let files = files.iter().map(|path| lopdf::Document::load(path).unwrap()).collect::<Vec<_>>();
        
        let mut document = pdf::merge(files).unwrap();
        document.save("merged.pdf").unwrap();
    }
}
