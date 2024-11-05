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

        if (isset($data['temperatura'], $data['fecha'], $data['cuna_id_cuna'])) {
            $stmt = $conn->prepare("INSERT INTO registroTemperatura (id_registroTemp, temperatura, fecha, cuna_id_cuna) 
                                    VALUES (:id_registroTemp, :temperatura, :fecha, :cuna_id_cuna)");

            $stmt->bindParam(':id_registroTemp', $data['id_registroTemp'], PDO::PARAM_INT);
            $stmt->bindParam(':temperatura', $data['temperatura']);
            $stmt->bindParam(':fecha', $data['fecha']);
            $stmt->bindParam(':cuna_id_cuna', $data['cuna_id_cuna'], PDO::PARAM_INT);

            if ($stmt->execute()) {
                echo json_encode(["message" => "Datos de registro de temperatura insertados exitosamente"]);
            } else {
                echo json_encode(["message" => "Error al insertar los datos de registro de temperatura"]);
            }
        } else {
            echo json_encode(["message" => "Datos incompletos en el JSON recibido"]);
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        $stmt = $conn->prepare("SELECT id_registroTemp, temperatura, fecha, cuna_id_cuna FROM registroTemperatura");
        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if ($result) {
            echo json_encode($result);
        } else {
            echo json_encode(["message" => "No se encontraron datos de registro de temperatura"]);
        }
    } else {
        echo json_encode(["message" => "Método no permitido"]);
    }
} catch (PDOException $e) {
    echo json_encode(["error" => "Error en la conexión: " . $e->getMessage()]);
}

$conn = null;
?>
