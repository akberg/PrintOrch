
/// Finite State Machine to track progess
/// 
/// Sheet file names are "[Composer - ][Title - ]Part"
pub struct FSM {
    pub in_dir: Option<std::path::PathBuf>,
    pub out_dir: Option<std::path::PathBuf>,
    pub out_name: String,
    pub docs: Vec<crate::instrument::Part>,
}

impl FSM {
    /// Refresh directory content
    pub fn update() {
        /* Refresh directory content */
    }
    pub fn avail_actions(&self) {
        
    }
    pub fn sort_files(&mut self) {
        self.docs.sort_by_key(|part| part.path.clone())
    }
    /// Load files into memory for merging, returning a tuple of Document and
    /// the number of times it should be added
    pub fn load_files(&self) -> Vec<(u32, lopdf::Document)> {
        self.docs
            .iter()
            .map(
                |crate::instrument::Part { path, n_copies, .. }| 
                (*n_copies, lopdf::Document::load(path).unwrap())
            )
            .collect::<Vec<_>>()
    }
}