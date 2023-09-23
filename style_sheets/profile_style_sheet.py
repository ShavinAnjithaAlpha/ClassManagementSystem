style_sheets = """   
        
        QPushButton {button-layout : 2;}
        
        QWidget#base {background-color : rgb(255, 255, 255)}
        
        QLabel {font-family : Helvetica;
                font-size : 20px;
                margin : 10px;
                color  : rgb(100, 100, 100)}
                
        QLabel#item_label {color  : rgb(0, 100, 250);
                        font-size : 22px;
                        margin-left : 20px;}
                
        QPushButton#edit_button {background : none;
                    color : blue;
                    font-size : 14px;
                    border : none;
                    }
                    
        QLineEdit {border : 3px solid blue;}
                    
        QPushButton#edit_button:hover , QPushButton#edit_button:pressed {color : rgb(0, 0, 100);}
                    
        QGroupBox::title {font-size : 18px;
                        border : none;}
                        
        QGroupBox {
                    border: 1px solid rgb(200, 200, 200);
                    font-size : 16px;
                    border-radius: 5px;
                    margin-top: 1ex; /* leave space at the top for the title */
}
                        
        QLabel#des_label {font-size : 16px;
                            color : rgb(150, 150, 150);}
                            
        QLineEdit#passwordBox {border : 1px solid blue;}
                            
        QLineEdit#passwordBox:focus {border : none;
                                    border-bottom : 2px solid blue;}
            
            """