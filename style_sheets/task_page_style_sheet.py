style_sheet = """
            QWidget#side_panel {background-color : blue;}
            
            QWidget#newTaskPanel {background-color : white;}
            
            QLabel {
                font-size : 22px;
                margin : 10px;}
                
            QTimeEdit , QDateEdit {
                font-size : 22px;
                padding : 7px;}
            
            QLineEdit#title_edit {
                    background : none;
                    color : black;
                    min-width : 800px;
                    font-size : 55px;
                    padding : 20px;
                    border : 1px solid rgb(230, 230, 230);
                    border-radius : 0px;}
                    
            QLineEdit#title_edit:focus {border-bottom : 3px solid black}
            
            QTextEdit {font-size : 20px;
                        width : 600px;
                        background : none;
                        border : 1px solid rgb(230, 230, 230);}
                        
            QPushButton#newSubTaskButton {
                        background-color : rgb(0, 200, 250);
                        padding : 10px;
                        color : black;
                        font-size : 22px;
                        border-radius : 0px;
                        border : none;
                        width : 200px;
                        text-alignment : left}
                        
            QPushButton#newSubTaskButton:hover {
                    background-color : rgb(0, 150, 250)}
                    
            QLineEdit#sub_task_edit {
                    padding : 20px;
                    background-color : rgb(200, 200, 220);
                    border-radius : 0px;
                    border : none;
                    font-size : 20px;}
                    
            QPushButton#new_task_button {
                        background-color : rgb(0, 250, 70);
                        color : black;
                        font-size : 25px;
                        border-radius : 5px;
                        border : none;
                        }
                        
            QPushButton#new_task_button:hover {background-color : rgb(0, 200, 100)}
            
            QLabel#label {
                    
                    color : rgb(200, 200, 250);
                    font-size : 15px;}
                    
            QPushButton#changeButton {
                    border : none;
                    background : none;
                    font-size : 25px;
                    color : white;
                    text-align : left}
                    
            QPushButton#changeButton:pressed {
                    background-color : rgb(20,20, 80)}
                    
            QPushButton#changeButton:hover {
                    border : 1px solid rgb(40, 0, 150)}
                    
            QScrollArea {
                        border : none;}
            
            QWidget#scroll_area_widget {background-color : blue}
                    
                """