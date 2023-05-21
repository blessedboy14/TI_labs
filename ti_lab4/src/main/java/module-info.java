module com.example.ti_lab4 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.ti_lab4 to javafx.fxml;
    exports com.example.ti_lab4;
}