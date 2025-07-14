<?php
// Данный файл позволяет проще вызывать скрипт https://chugunka10.net/img/resize-png.php

// https://chugunka10.net/img/dir-resize.php



// header('Content-Type: text/plain');
header('Content-Type: text/html');
header('Cache-Control: no-cache,must-revalidate');
// header("Content-Security-Policy: default-src 'none'; 'style-src 'self'; script-src 'self'; img-src 'self'");
header("Content-Security-Policy: default-src 'none'; style-src 'self';");

?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Поиск изображений для преобразования</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
<?php

function path_join($base, $path)
{
    return rtrim($base, '/') . '/' . $path;
}

function isSubPath($parentPath, $subPath)
{
    $rpp = path_join(realpath($parentPath), '');
    $len = strlen($rpp);

    $index = strncmp($rpp, realpath($subPath) . "/", $len);
    return $index == 0;
}


$TopDir = realpath(getcwd());
if ($TopDir[$len - 1] != '/')
    $TopDir .= "/";

if (!isset($_GET['dir']) || strlen($_GET['dir']) == 0)
{
    $curDir = ".";
}
else
{
    $curDir = $_GET['dir'];

    if (!isSubPath($TopDir, $curDir) || !is_dir($curDir))
    {
        die("ERROR: dir must be a subdir in the 'img' dir");
    }
}

function str_ends_with($str, $end)
{
    // Если искомая подстрока пустая, возвращаем true
    if (empty($end))
    {
        return true;
    }
    
    // Находим позицию последнего вхождения подстроки
    $position = strrpos($str, $end);
    
    // Проверяем, совпадает ли позиция с концом строки
    return ($position !== false && $position === strlen($str) - strlen($end));
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

function ListDir($curDir)
{
    echo "Директория $curDir<br><br>";

    // $files = glob($directory . $pattern);
    $files = scandir($curDir);

    if (realpath($TopDir) != realpath($curDir))
    {
        $up = dirname($curDir);
        echo "<a href='https://chugunka10.net/img/dir-resize.php?dir=$up'>Вверх</a><br>";
    }

    // Этого никогда не бывает, ибо "." и ".." всегда обнаружатся.
    if (!$files)
    {
        echo "<br><strong>Не обнаружено файлов и директорий</strong><br>";
        return;
    }

    $containsDir = false;
    foreach ($files as $file)
    {
        if ($file == "." or $file == "..")
            continue;

        if ($curDir == ".")
            $file_full = $file;
        else
            $file_full = path_join($curDir, $file);

        if (is_dir($file_full))
        {
            if (!$containsDir)
            {
                $containsDir = true;
                echo "<br><hr>Папки:<br>";
            }

            $newDir = $file_full;
            echo "<a href='https://chugunka10.net/img/dir-resize.php?dir=$newDir'>$file</a><br>";
        }
    }

    $containsFiles = false;
    $colorNumber   = 0;
    foreach ($files as $file)
    {
        if ($file == "." or $file == "..")
            continue;
        
        if ($curDir == ".")
            $file_full = $file;
        else
            $file_full = path_join($curDir, $file);

        if (is_file($file_full))
        if (str_ends_with($file, '.png'))
        {
            if (str_ends_with($file, '.r.png'))
                continue;

            $sizes = [2000, 1600, 1200, 800, 400, 200];
            $thlen = count($sizes)+1;
            if (!$containsFiles)
            {
                $containsFiles = true;
                echo "<br><hr>";
                echo "<table>";
                echo "<tr><th>Файлы</th><th colspan=\"$thlen\">Размеры</th></tr>";
            }

            $color = "lg1";
            if ($colorNumber == 1)
            {
                $color = "lg2";
                $colorNumber = 0;
            }
            else
            {
                $colorNumber = 1;
            }
            
            $file      = htmlspecialchars($file);
            $file_full = lightUrlEncode($file_full);
            echo "<tr class=$color>";
            echo "<td><a target=_blank href='https://chugunka10.net/img/resize-png.php?path=$file_full'>$file</a></td>";
            echo "<td>    </td>";
            foreach ($sizes as $size)
            {
                echo "<td class=size><a target=_blank href='https://chugunka10.net/img/resize-png.php?maxh=$size&maxw=$size&path=$file_full'>$size</a></td>";
            }
            echo "</tr>";
        }
    }
    if ($containsFiles)
    {
        echo "</table>";
    }
    
    if (!$containsDir and !$containsFiles)
    {
        echo "<br><strong>Не обнаружено файлов и директорий</strong><br>";
        return;
    }
}



ListDir($curDir);


?>
</body>
</html>
