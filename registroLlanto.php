<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "cunainteligente";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);

        if (isset($data['id_registroLlanto'], $data['llanto'], $data['razon'], $data['fecha'], $data['cuna_id_cuna'])) {
            $stmt = $conn->prepare("INSERT INTO registroLlanto (id_registroLlanto, llanto, razon, fecha, cuna_id_cuna) 
                                    VALUES (:id_registroLlanto, :llanto, :razon, :fecha, :cuna_id_cuna)");

            $stmt->bindParam(':id_registroLlanto', $data['id_registroLlanto'], PDO::PARAM_INT);
            $stmt->bindParam(':llanto', $data['llanto']);
            $stmt->bindParam(':razon', $data['razon']);
            $stmt->bindParam(':fecha', $data['fecha']);
            $stmt->bindParam(':cuna_id_cuna', $data['cuna_id_cuna'], PDO::PARAM_INT);

            if ($stmt->execute()) {
                echo json_encode(["message" => "Datos de registro de llanto insertados exitosamente"]);
            } else {
                echo json_encode(["message" => "Error al insertar los datos de registro de llanto"]);
            }
        } else {
            echo json_encode(["message" => "Datos incompletos en el JSON recibido"]);
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        $stmt = $conn->prepare("SELECT id_registroLlanto, llanto, razon, fecha, cuna_id_cuna FROM registroLlanto");
        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if ($result) {
            echo json_encode($result);
        } else {
            echo json_encode(["message" => "No se encontraron datos de registro de llanto"]);
        }
    } else {
        echo json_encode(["message" => "Método no permitido"]);
    }
} catch (PDOException $e) {
    echo json_encode(["error" => "Error en la conexión: " . $e->getMessage()]);
}

$conn = null;
?>
