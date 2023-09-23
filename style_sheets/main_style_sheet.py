main_style_sheet = """
                
                QWidget {font-family : segoe UI;
                        font-weight : 18px;}                    
                
                QWidget#mainPage {background-image : url(images/system_images/wallpaper.jpg);
                                background-position : center center;}
                
                QWidget#sidePanel {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgba(30, 0, 50, 0.8) ,stop : 1 rgba(20, 0, 250, 0.8));
                                border-radius : 5px;}
                
                QPushButton {background-color :blue;
                            color  : white;
                            border : 1px solid rgb(0, 0, 200);
                            font-size : 18px;
                            padding : 15px;
                            border-radius : 5px;
                            widget-animation-duration : 800ms;
                            button-layout : 2;
                            }
                            
                QPushButton:focus {border : 2px solid rgb(0, 100, 200);}
                
                QPushButton:hover {background-color : rgb(0, 0, 200)}
                
                QPushButton:pressed {background-color : rgb(0, 0 ,150);
                                    color : rgb(150, 150, 150)}
                
                QPushButton:disabled {background-color : rgb(0, 0, 130)}
                            
                QPushButton#mainButtons {background-color : rgba(250,250, 250, 0.6);
                                        color : black;
                                        border  : none;
                                        border-radius : 5px;
                                        margin : 5px;
                                        }
                                        
                QPushButton#mainButtons:hover  , QPushButton#mainButtons:pressed 
                                        {background : QLinearGradient(spread:pad,  x1 : 0 , y1 : 0 , x2 : 0, y2 : 1, stop : 0 rgba(0, 10, 100, 0.5) , stop : 0.5 rgba(15, 15, 170, 0.5) ,stop : 1 rgba(30, 0, 250, 0.5));
                                        color  :white;
                                        font-weight : bold;
                                        border-radius : 5px;}
                
                QPushButton#side_panel_action {background : none;
                                                border : none;
                                                font-size : 22px;
                                                margin : 10px;
                                                border-radius : 15px;
                                                height : 30px;
                                                width : 100px;
                                                padding : 8px;}
                                                
                QPushButton#side_panel_action:hover {background-color  : rgb(0, 0, 100);}
                
                QPushButton#side_panel_action:pressed {background-color : rgb(0, 0, 150);
                                                        font-weight  :bold}
                
                QPushButton#profileButton {background-color : blue;
                                            border : 2px solid blue;
                                            color : white;
                                            padding : 10px;
                                            border-radius : 5px;
                                            }
                QPushButton#profileButton:hover {background-color : rgb(0, 50, 150)}
                
                QPushButton#notRoundButton {border-radius : 0px;}
                                        
                QLabel {background : none;}
                
                QLabel#timeLabel {color : rgb(0, 200, 50)}
                
                QLabel#name_label {color : white;
                                    margin : 25px;}
                
                QLabel#welcomeLabel {color : yellow}
        
                QLineEdit {background-color  : white;
                            padding : 7px;
                            font-size : 18px;
                            border : 1px solid rgb(150, 150, 150);
                            border-radius : 5px;}
                
                QLineEdit:hover {color : rgb(50, 50, 50);
                                border-color  :rgb(0, 0, 200);}
                
                QLineEdit:focus {border : 2px solid blue;
                                background-color  : rgba(255, 255, 255);}
                
                QDateEdit {padding : 7px;
                            font-size : 16px;}
                            
                QRadioButton , QCheckBox {font-size : 15px;
                                padding : 5px;
                                margin : 5px;}
                
                QComboBox {padding  : 7px;
                            font-size : 18px;
                            border : 1px solid blue;
                            padding : 5px;
                            border-radius : 5px;}
                            
                QComboBox::drop-down {background : none;
                                    border : none;}
                            
                QComboBox::down-arrow {background : none;
                                        border : none;}
                            
                QComboBox QAbstractItemView {font-size : 17px;
                                            background-color  :white;
                                            padding : 7px;
                                            border-radius : 5px;}
                                            
                QComboBox QAbstractItemView:item {border-bottom : 1px solid blue;
                                                    padding-bottom : 5px;
                                                    border-radius : 5px;}
                                                    
                QComboBox QAbstractItemView:text {border : 1px solid black;}
                            
               
                
                            
                QSpinBox , QDoubleSpinBox {font-size : 16px;
                            padding : 7px;}
                            
                QListWidgetItem {font-size : 16px;
                            border-radius : 3px;}
                            
                QDialog {background-color : rgb(255, 255, 255)}
                
                QDialog QPushButton {background-color : blue;
                                    padding : 7px;
                                    color  :white;}
                                    
                QDialog QPushButton:hover {background-color : rgb(0, 0, 200);}
                
                QDialog QLabel {font-size : 16px;} 
                
                QInputDialog QLineEdit {min-width : 300px;
                                        padding : 5px;}
                                        
                QMessageBox QLabel {font-size : 15px;}
                
                QMessageBox QPushButton {width : 100px;}
                                        
                QHeaderView::section {background-color : rgb(0, 100, 250);
                                    border : none;
                                    color : white;
                                    border-right : 1px solid rgb(0, 200, 250);
                                    border-bottom : 1px solid blue;
                                    padding : 5px;}
                                    
                QHeaderView::section:selected {font-weight  :bold;}
                                    
                QTableView::section {background-color : orange;}
                
                
                QListView {background-color : white;
                            border-radius : 7px;
                            border : 1px solid rgb(150, 150, 150);}
                            
                QListView::item {background-color: white;
                                font-size : 17px;
                                border-bottom : 1px solid rgb(200, 200, 200);
                                border-radius : 7px;
                                padding : 5px;}
                
                QListView::item:selected {background-color : blue;
                                            color : white;}
                
                QListView QCheckBox::indicator {min-width : 20px;
                                                min-height : 20px;}
                
                QTableView {selection-background-color: rgb(0, 0, 150);
                            font-size : 16px;
                            padding : 5px;}
                            
                QLineEdit#new_task_field {
                                background-color : rgba(20, 0, 80, 0.8);
                                padding : 25px;
                                min-height : 30px;
                                font-size : 22px;
                                color : white;
                                border : none;
                                border-radius : 0px;
                                margin : 0px;}
                                
                QPushButton#plus_button {background : rgba(20, 0, 80, 0.8);
                                    font-size : 25px;
                                    padding : 12px;
                                    color : white;
                                    border : none;
                                    border-radius : 0px;}
                
                QDateTimeEdit {
                        padding : 7px;
                        font-size : 20px;}
                
                        """