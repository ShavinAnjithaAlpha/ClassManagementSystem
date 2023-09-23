style_sheet = """
            
            
            QPushButton#weekDayButton {
                                background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgb(0, 100, 240),
                                                                    stop : 1 rgb(0, 50, 250));
                                padding : 5px;
                                margin : 0px;
                                font-family : verdana;
                                color : white;
                                font-size : 22px;
                                border-radius : 0px;
                                border : none;
                                border-right : 1px solid blue;}
                                
                                
            QPushButton#weekDayButton:hover {
                                background-color : rgb(0, 120, 250);
                                border-bottom : 4px solid rgb(240, 50, 0)}
                                
            QPushButton#dayButton {
                        background-color : rgb(255, 255, 255);
                        border : 1px solid rgb(240, 240, 240);
                        padding : 5px;
                        font-size : 25px;
                        font-weight : bold;
                        color : black;
                        border-radius : 0px;
                        margin : 0px;}
                        
            QPushButton#dayButtonToday {background-color : rgba(200, 0, 100, 0.8);
                                        border : 2px solid rgb(250, 0, 0);
                                        padding : 5px;
                                        font-size : 25px;
                                        font-weight : bold;
                                        border-radius : 0px;
                                        margin : 0px;}
                                        
            QPushButton#dayButtonToday:hover {
                            border : 4px solid orange;}
                        
            QPushButton#dayButton:hover {
                        background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 :0, stop : 0 rgb(240, 70, 0), 
                                                            stop : 1 rgb(250, 120, 0));
                        border-color : rgb(255, 0, 50);
                        border-width : 5px;}
                                
            QLabel#present_date_label {
                            padding : 20px;
                            font-size : 55px;
                            font-family : Helvetica;
                            background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(250, 0, 0),
                                                                stop : 0.5 rgba(250, 70, 0, 0.9), stop : 1 rgba(250, 100, 0, 0.9));
                            background-position : center center;
                            opacity : 0.5;
                            color : white;
                            font-weight : bold;}
                            
            QLabel#yearLabel , QLabel#monthLabel {
                    font-size : 30px;
                    padding : 10px;}
                    
            QSpinBox {
                    font-size : 22px;}
                    
            QComboBox {font-size : 20px;}
            
            QLabel#clickedDateLabel {
                    background-color : blue;
                    padding : 20px;
                    margin : 0px;
                    font-size : 25px;
                    color : white;}
            
            QPushButton#arrowButton {
                        background : none;
                        border-right : 1px solid rgb(0, 0, 100);
                        border-left : 1px solid rgb(0, 0, 100);
                        border-radius : 0px;
                        font-size : 30px;
                        font-weight : bold;
                        margin : 0px;
                        padding : 5px;
                        color : black;
                        height : 50px;}
                        
            QPushButton#arrowButton:hover {
                        background-color : blue;
                        color : white;
                        }
            
            """