Nice. A short, tight PRD plus acceptance criteria will make Claude much more precise and reduce hallucinated features. Here you go.

---

## **Product Requirements Document (PRD)**

**Project name:** Album Planner
**Purpose:** A simple desktop app to organise MP3 files into album tracklists and prepare them for CD burning or release.

---

### **1. Problem**

I create many MP3 tracks and need a fast way to organise them into albums. Current file explorers are slow, error-prone, and do not track total duration or allow easy reordering. I want a focused tool that lets me drag, reorder, and export tracks while ensuring the album fits within an 80-minute CD limit.

---

### **2. Target User**

Independent music creators and producers who want to plan albums quickly without complex DAW or music library software.

---

### **3. Goals**

The app should:

* Allow fast drag-and-drop album creation.
* Provide real-time duration tracking.
* Make track reordering easy.
* Export a correctly ordered and renamed album folder.
* Be simple and lightweight.

---

### **4. Scope (MVP)**

#### **4.1 Import Tracks**

* Users drag and drop MP3 files into the app.
* The app reads:

  * Track title (from metadata if available).
  * Duration.
* Files appear in a list.

#### **4.2 Track List**

Each track row displays:

* Track number.
* Title.
* Duration.
* Original filename.

#### **4.3 Reordering**

* Users reorder tracks via drag-and-drop.

#### **4.4 Album Duration**

The app shows:

* Total running time.
* Remaining time up to 80 minutes.
* Visual warning if exceeded.

#### **4.5 Album Metadata**

Users can enter:

* Band name.
* Album name.

#### **4.6 Export Album**

When the user clicks **Create Album**:

* A folder is created named after the album.
* Tracks are copied (not moved).
* Tracks are renamed:

  * `01. Song Title.mp3`
  * `02. Song Title.mp3`
* Titles come from metadata, fallback to filename.

---

### **5. Non-Functional Requirements**

* Must run on Windows.
* Prefer cross-platform if low effort.
* Must be fast and stable.
* Minimal setup.
* Simple UI.

---

### **6. Out of Scope (MVP)**

* Audio editing.
* CD burning.
* Metadata editing.
* Streaming or library management.

---

### **7. Future Features**

* Save/load album projects.
* CD burner integration.
* Metadata editing.
* WAV and FLAC support.
* Playlist export.
* Multiple album versions.
* Export for digital platforms.

---

## **Acceptance Criteria**

### **Import**

* User can drag multiple MP3 files into the app.
* Files are loaded and displayed.

### **Metadata**

* Duration and title display correctly.
* Missing metadata falls back to filename.

### **Reordering**

* Tracks can be reordered visually.
* Order updates instantly.

### **Duration Tracking**

* Total duration updates in real time.
* Warning shown when over 80 minutes.

### **Album Info**

* User can input album and band name.

### **Export**

* Folder created successfully.
* Files copied and renamed in order.
* Filenames numbered correctly.
* Invalid characters removed automatically.

### **Usability**

* Interface is clear and minimal.
* No crashes during normal workflow.

