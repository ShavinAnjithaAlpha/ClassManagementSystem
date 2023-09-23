style_sheet = """
            QLabel {font-size : 18px;
                    font-family : verdana;
                    background : none;
                    }
                    
            QLabel#name_label {background-color  :blue;
                            margin : 0px;
                            padding : 20px;
                            font-size : 35px;
                            border-right : 1px solid rgb(0, 0, 150)}
                            
            QLabel#grade_label {font-size : 22px;
                                background-color  :blue;
                                margin : 0px;
                                padding : 20px;
                                color  :white;
                                border-right : 1px solid rgb(0, 0, 150)}
                                
            QLabel#date_label {font-size : 18px;
                                background-color : blue;
                                margin : 0px;
                                padding : 20px;
                                color  :white}
            
            
            QLabel#field_label {font-size : 22px;
                                color : white;
                                padding : 20px;
                                background-color  : rgb(0, 0, 150);
                                }
                                
            QLabel#value_label {
                                font-size : 34px;
                                color  :white;
                                padding : 10px;
                                background-color  : rgb(0, 0, 150)}
            
            
            QListView::item {border : none;
                                background : none;
                                border-radius : 0px;
                                margin : 5px;}
                                
            QListView::item:selected {background : none;}
            
            QCheckBox {font-size : 17px;}
            
            QCheckBox::indicator:checked {border-radius : 3px;
                                            background-color : rgb(0, 200, 50);
                                            width : 30px;
                                            height : 30px;}
                                            
            QCheckBox::indicator:!checked {background-color  : red;
                                                width : 30px;
                                                height : 30px;}
            QCheckBox::indicator:hover {border : 1px solid blue;}
                                

"""