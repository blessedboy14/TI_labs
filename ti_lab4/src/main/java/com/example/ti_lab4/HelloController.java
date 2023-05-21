package com.example.ti_lab4;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.input.KeyEvent;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.stage.Window;
import java.io.*;
import java.math.BigInteger;
import java.util.Arrays;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class HelloController {
    private int dValue;
    private int pValue;
    private final int H0 = 100;
    private long rValue;
    private long eulerFunc;
    private int qValue;
    private int eValue;
    private int[] inputSequence = new int[0];
    private String inputFilePath;
    @FXML
    private TextField eInput;
    @FXML
    private TextField qInput;
    @FXML
    private TextField pInput;
    @FXML
    private TextArea plainText;
    @FXML
    private TextArea signText;
    private void convertBytes(byte[] bytes) {
        inputSequence = new int[bytes.length];
        for (int i = 0; i < bytes.length; i++) {
            inputSequence[i] = bytes[i] & 0xFF;
        }
    }
    @FXML
    private void openFile() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Открыть");
        File file = fileChooser.showOpenDialog(new Stage());
        if (file != null) {
            inputFilePath = file.getPath();
            byte[] inputBytes = new byte[(int) file.length()];
            try (FileInputStream fileInputStream = new FileInputStream(file.getPath())) {
                fileInputStream.read(inputBytes, 0, inputBytes.length);
            } catch (IOException e) {
                e.printStackTrace();
            }
            convertBytes(inputBytes);
            String inputString = Arrays.toString(inputSequence).substring(1,Arrays.toString(inputSequence).length()-1);
            inputString = inputString.replace("," ," ");
            signText.setText("");
            plainText.setText(inputString.length() < 5000 ? inputString : inputString.substring(0, 5000));
        }
    }
    @FXML
    private void openSignFile() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Открыть файл с подписью");
        File file = fileChooser.showOpenDialog(new Stage());
        boolean isInputOk = false;
        long signature = 0;
        if (file != null) {
            try (BufferedReader br = new BufferedReader(new FileReader(file.getPath()))) {
                signature = Long.parseLong(br.readLine());
                isInputOk = true;
            } catch (IOException e) {
                e.printStackTrace();
            }
            if (isInputOk) {
                signText.setText(String.valueOf(signature));
            } else {
                makeAlert("Неверный ввод подписи", Alert.AlertType.WARNING, "Warning", "Some error was found");
            }
        }
    }
    private void makeAlert(String text, Alert.AlertType type, String title, String header) {
        Alert alert = new Alert(type);
        alert.initOwner(Stage.getWindows().stream().filter(Window::isShowing).toList().get(0));
        alert.setTitle(title);
        alert.setHeaderText(header);
        alert.setContentText(text);
        alert.showAndWait();
    }
    private boolean isInputCorrect(String input, String validRegEx, int maxValue, int minValue, boolean forPrime) {
        Pattern pattern = Pattern.compile(validRegEx);
        Matcher matcher = pattern.matcher(input);
        if (matcher.matches()) {
            int intVal;
            try {
                intVal = Integer.parseInt(input);
            } catch (NumberFormatException e) {
                return false;
            }
            return Integer.parseInt(input) < maxValue
                    && Integer.parseInt(input) > minValue && (OperationBox.isLittleNumberPrime(intVal) || !forPrime);
        }
        return false;
    }
    @FXML
    private void initialize () {
        eInput.setDisable(true);
        signText.setEditable(false);
        plainText.setEditable(false);
        writeToFile();
    }
    private boolean isECorrect (String text, String validRegEx, long maxValue) {
        Pattern pattern = Pattern.compile(validRegEx);
        Matcher matcher = pattern.matcher(text);
        if (matcher.matches()) {
            int intVal;
            try {
                intVal = Integer.parseInt(text);
            } catch (NumberFormatException e) {
                return false;
            }
            return Integer.parseInt(text) < maxValue
                    && Integer.parseInt(text) > 1 && OperationBox.isPrimeWith(intVal, maxValue);
        }
        return false;
    }
    @FXML
    private void filerEInput(KeyEvent ev) {
        if (eInput.getText().length() > 0) {
            if (!isECorrect(eInput.getText(), "\\d+", eulerFunc)) {
                eInput.setStyle("-fx-text-box-border: #d60616; -fx-focus-color: #d60616;");
            } else {
                eInput.setStyle("-fx-text-box-border: ladder(\n" +
                        "        -fx-background,\n" +
                        "        black 10%,\n" +
                        "        derive(-fx-background, -15%) 30%\n" +
                        "    ); -fx-focus-color: #0093ff; -fx-border-width: 1px;");
            }
        } else {
            eInput.setStyle("-fx-text-box-border: ladder(\n" +
                    "        -fx-background,\n" +
                    "        black 10%,\n" +
                    "        derive(-fx-background, -15%) 30%\n" +
                    "    ); -fx-focus-color: #0093ff; -fx-border-width: 1px;");
        }
    }
    private void calculateRValue() {
        if (isInputCorrect(qInput.getText(), "\\d+", Integer.MAX_VALUE, 1, true)
                && isInputCorrect(pInput.getText(), "\\d+", Integer.MAX_VALUE, 1, true)
        && !Objects.equals(qInput.getText(), pInput.getText())) {
            rValue = Long.parseLong(pInput.getText()) * Long.parseLong(qInput.getText());
            eulerFunc = (Long.parseLong(pInput.getText()) - 1) * (Long.parseLong(qInput.getText()) - 1);
            eInput.setDisable(false);
        }
    }
    @FXML
    private void filerQInput(KeyEvent ev) {
        if (qInput.getText().length() > 0) {
            if (!isInputCorrect(qInput.getText(), "\\d+",
                    Integer.MAX_VALUE, 1, true)) {
                qInput.setStyle("-fx-text-box-border: #d60616; -fx-focus-color: #d60616;");
                eInput.setDisable(true);
            } else {
                calculateRValue();
                qInput.setStyle("-fx-text-box-border: ladder(\n" +
                        "        -fx-background,\n" +
                        "        black 10%,\n" +
                        "        derive(-fx-background, -15%) 30%\n" +
                        "    ); -fx-focus-color: #0093ff; -fx-border-width: 1px;");
            }
        } else {
            eInput.setDisable(true);
            qInput.setStyle("-fx-text-box-border: ladder(\n" +
                    "        -fx-background,\n" +
                    "        black 10%,\n" +
                    "        derive(-fx-background, -15%) 30%\n" +
                    "    ); -fx-focus-color: #0093ff; -fx-border-width: 1px;");
        }
    }
    @FXML
    private void filterPInput(KeyEvent ev) {
        if (pInput.getText().length() > 0) {
            if (!isInputCorrect(pInput.getText(), "\\d+", Integer.MAX_VALUE, 1, true)) {
                pInput.setStyle("-fx-text-box-border: #d60616; -fx-focus-color: #d60616;");
                eInput.setDisable(true);
            } else {
                calculateRValue();
                pInput.setStyle("-fx-text-box-border: ladder(\n" +
                        "        -fx-background,\n" +
                        "        black 10%,\n" +
                        "        derive(-fx-background, -15%) 30%\n" +
                        "    ); -fx-focus-color: #0093ff; -fx-border-width: 1px;");
            }
        } else {
            eInput.setDisable(true);
            pInput.setStyle("-fx-text-box-border: ladder(\n" +
                    "        -fx-background,\n" +
                    "        black 10%,\n" +
                    "        derive(-fx-background, -15%) 30%\n" +
                    "    ); -fx-focus-color: #0093ff; -fx-border-width: 1px;");
        }
    }
    private boolean fieldFill() {
        return isInputCorrect(qInput.getText(), "\\d+", Integer.MAX_VALUE, 1, true)
                && isInputCorrect(pInput.getText(), "\\d+", Integer.MAX_VALUE, 2, true)
                && isECorrect(eInput.getText(), "\\d+", eulerFunc)
                && inputFilePath != null;
    }
    private void setValuesFromInput(){
        this.pValue = Integer.parseInt(pInput.getText());
        this.eValue = Integer.parseInt(eInput.getText());
        this.qValue = Integer.parseInt(qInput.getText());
    }
    private void writeToFile() {
        try(FileOutputStream fileOutputStream = new FileOutputStream("C:\\Users\\USER\\Desktop\\file.txt")) {
            fileOutputStream.write(20);
            fileOutputStream.write(29);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    private void writeSignToFile(long signature) {
        String fileName = inputFilePath.split("\\.")[0] + "(sign).txt";
        try (PrintWriter writer = new PrintWriter(fileName, "UTF-8")) {
            writer.print(signature);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    @FXML
    private void onSignClick() {
        if (fieldFill()) {
            setValuesFromInput();
            this.dValue = (int) OperationBox.computeDValue(this.eValue, this.eulerFunc);
            System.out.println(this.dValue);
            long mValue = OperationBox.compressInputFile(this.H0, inputSequence, rValue);
            long signature = OperationBox.fastExp(mValue, dValue, rValue);
            signText.setText(String.valueOf(signature));
            writeSignToFile(signature);
            makeAlert("Результаты: открытый ключ(" + eValue + "," + rValue + "), " +
                            "закрытый ключ(" + dValue + "," + rValue + "), " + "m(хеш-образ из файла) = "
                            + mValue + ", подпись = " + signature, Alert.AlertType.INFORMATION, "Успех!",
                    "Документ успешно подписан, результаты ниже");
        } else {
            makeAlert("Неверный ввод", Alert.AlertType.WARNING, "Warning", "Произошла некоторая ошибка");
        }
    }
    @FXML
    private void onCheckClick() {
        if (fieldFill() && signText.getText().length() > 0) {
            setValuesFromInput();
            long signature = Long.parseLong(signText.getText());
            this.dValue = (int) OperationBox.computeDValue(this.eValue, this.eulerFunc);
            long mValue = OperationBox.compressInputFile(this.H0, inputSequence, rValue);
            long sValue = OperationBox.fastExp(signature, eValue, rValue);
            boolean isSignCorrect = mValue == sValue;
            if (isSignCorrect) {
                makeAlert("Результаты: открытый ключ(" + eValue + "," + rValue + "), " +
                                "закрытый ключ(" + dValue + "," + rValue + "), " + "m(хеш-образ из файла) = " + mValue +
                        ", S(хеш-образ из подписи) = " + sValue, Alert.AlertType.INFORMATION, "Успех!",
                        "Подпись верна, результаты ниже");
            } else {
                makeAlert("Результаты: открытый ключ(" + eValue + "," + rValue + "), "  +
                                "закрытый ключ(" + dValue + "," + rValue + "), " + "m(хеш-образ из файла) = " + mValue +
                                ", S(хеш-образ из подписи) = " + sValue, Alert.AlertType.INFORMATION, "Неудача!",
                        "Подпись неверна, результаты ниже");
            }
        } else {
            makeAlert("Неверный ввод", Alert.AlertType.WARNING, "Warning", "Произошла некоторая ошибка");
        }
    }
    private byte calculateBlockSize(int rValue) {
        byte size = 1;
        int temp = pValue >> 8;
        while (temp > 0) {
            size++;
            temp = temp >> 8;
        }
        return size;
    }
}