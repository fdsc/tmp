<?php
// Данный файл производит изменение размера изображения, генерируя сразу два уменьшенных изображения

// https://chugunka10.net/img/resize-png.php?path=1961/16-12.png

// /home/srv210412/chugunka10.net/img
// echo "Текущая директория ";
// echo getcwd();
// list($width, $height, $type, $attr) = getimagesize($imagePath);



// header('Content-Type: text/plain');
header('Content-Type: text/html');
header('Cache-Control: no-cache,must-revalidate');
header("Content-Security-Policy: default-src 'none'; style-src 'self';");

?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Преобразование изображения</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<?php  
$originalImagePath  = $_GET['path'];
// $originalImagePath = '1961/16-12.png';
if (!isset($originalImagePath))
{
    exit("Путь к изображению не указан.<br><br>Примеры работы с данным файлом:<br>https://chugunka10.net/img/resize-png.php?path=1961/16-12.png<br>https://chugunka10.net/img/resize-png.php?maxw=600&maxh=400&maxwp=1600&maxhp=1024&path=1961/16-12.png<br>");
}


function lightUrlEncode($path)
{
    $symbols = ["<", ">", "?", "#", "&"];
    foreach ($symbols as $symbol)
    {
        $path = str_replace($symbol, urlencode($symbol), $path);
    }
    
    return $path;
}

// Функция уменьшает изображение, сохраняя пропорции
function resize($originalImagePath, $maxW, $maxH)
{
    $originalImagePath_html = htmlspecialchars($originalImagePath);
    //if (strcmp($htmlspecialchars_html, $originalImage) != 0)
    //    die("ERROR: unknown error j2FGdl");

    // Загрузка оригинального изображения
    $originalImage = imagecreatefrompng($originalImagePath);

    if (empty($originalImage))
    {
        exit("Не удалось загрузить изображение \"$originalImagePath_html\"<br><br>");
    }
    else
    {
        echo '<table>';
        echo '<tr>';
        echo "<td class=c>$originalImagePath_html</td><td>Имя оригинального изображения</td>";
        echo '</tr>';
    }

    $width  = imagesx($originalImage);
    $height = imagesy($originalImage);
    echo '<tr>';
    echo "<td class=c>$width x $height</td><td>Размер оригинального изображения</td>";
    echo '</tr>';

    // Находим коэффициент масштабирования
    $kW = $width  / $maxW;
    $kH = $height / $maxH;    
    $k  = max($kW, $kH);
    
    if ($k <= 1.0)
    {
        imagedestroy($originalImage);
        echo "</table><strong>Изображение слишком маленькое для уменьшения до размера $maxW x $maxH</strong><br><br><br>";
        return;
    }

    // Желаемая ширина и высота нового изображения
    $newWidth  = round($width  / $k);
    $newHeight = round($height / $k);

    // Вычисляем путь к новому файлу
    $resizedImagePath  = substr($originalImagePath, 0, strlen($originalImagePath) - 4);
    $resizedImagePath .= "-" . max($newWidth, $newHeight);
    $resizedImagePath .= ".r.png";
    if (!file_exists($resizedImagePath))
    {
        // Создание нового холста с заданными размерами
        $newImage = imagecreatetruecolor($newWidth, $newHeight);

        // Копирование и изменение размера изображения
        imagecopyresampled($newImage, $originalImage, 0, 0, 0, 0, 
                           $newWidth, $newHeight, 
                           imagesx($originalImage), imagesy($originalImage));

        // Сохранение нового изображения в файл
        imagepng($newImage, $resizedImagePath);

        // Освобождение памяти
        imagedestroy($newImage);
        echo '<tr>';
        echo "<td class='c b'>$newWidth x $newHeight</td><td>Изображение успешно уменьшено до разрешения</td>";
        echo '</tr>';
    }
    else
    {
        echo '<tr>';
        echo "<td class='c b'>$newWidth x $newHeight</td><td>Запрашиваемое изображение уже существует в этом разрешении</td>";
        echo '</tr>';
    }
    echo '</table>';
    imagedestroy($originalImage);

    $url      = 'https://chugunka10.net/img/' . lightUrlEncode($resizedImagePath);
    $url_html = 'https://chugunka10.net/img/' . htmlspecialchars($resizedImagePath);
    $resizedImagePath_html = htmlspecialchars($resizedImagePath);
    echo "<br>Имя нового файла \"$resizedImagePath_html\"<br><hr>Сетевое имя файла для размера <strong>$newWidth x $newHeight</strong>:<br><a target=_blank href=\"$url\">$url_html</a><br><hr><br><br><br>";
}

$maxW  = $_GET['maxw'];
$maxH  = $_GET['maxh'];
$maxWp = $_GET['maxwp'];
$maxHp = $_GET['maxhp'];

if (!isset($_GET['maxw']))
{
    $maxW = 1200;
}
if (!isset($_GET['maxh']))
{
    $maxH = 1200;
}


resize($originalImagePath, $maxW, $maxH);


if (!isset($_GET['maxwp']))
{
    $maxWp = 600;
}
if (!isset($_GET['maxhp']))
{
    $maxHp = 600;
}

// if (isset($maxHp) && isset($maxHp))
{
    resize($originalImagePath, $maxHp, $maxHp);
}


?>
</body>
</html>
