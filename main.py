import os
import json
from datetime import datetime
import qrcode

# === Настройки ===
HISTORY_FILE = "history.json"
OUTPUT_DIR = "qr_images"

# === Инициализация ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# === Функции ===

def get_filename():
    """Автоматическое имя файла с датой"""
    return f"qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

def save_history(text, filename, success):
    """Сохраняет историю в JSON"""
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
    
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
        "file": filename,
        "success": success
    })
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def show_history():
    """Показывает историю"""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        print("История пуста")
        return
    
    if not history:
        print("История пуста")
        return
    
    print("\n=== ПОСЛЕДНИЕ ОПЕРАЦИИ ===")
    for item in history[-5:]:  # Показываем последние 5
        status = "✅" if item["success"] else "❌"
        print(f"{status} {item['time']} - {item['text'][:30]}... -> {item['file']}")
    print()

def generate_qr():
    """Главная функция генерации QR-кода"""
    print("\n--- ГЕНЕРАЦИЯ QR-КОДА ---")
    
    # 1. Ввод текста (с проверкой на пустоту)
    text = input("Введите текст или URL: ").strip()
    if not text:
        print("❌ Ошибка: текст не может быть пустым!")
        return
    
    # 2. Проверка длины (максимум 1000 символов)
    if len(text) > 1000:
        print("❌ Ошибка: текст слишком длинный (макс. 1000 символов)!")
        return
    
    # 3. Настройки (по умолчанию, можно менять)
    print("\nПараметры (оставьте Enter для значений по умолчанию):")
    
    version = input("Версия (1-40, Enter=авто): ")
    version = int(version) if version.isdigit() and 1 <= int(version) <= 40 else None
    
    ec = input("Коррекция (L/M/Q/H, Enter=M): ").upper()
    ec = ec if ec in ['L','M','Q','H'] else 'M'
    
    box = input("Размер модуля (Enter=10): ")
    box = int(box) if box.isdigit() and int(box) > 0 else 10
    
    # 4. Имя файла
    name = input("Имя файла (без .png, Enter=авто): ").strip()
    filename = f"{name}.png" if name else get_filename()
    
    # Проверка на конфликт имен
    filepath = os.path.join(OUTPUT_DIR, filename)
    counter = 1
    while os.path.exists(filepath):
        name_base = filename.replace(".png", "")
        filename = f"{name_base}_{counter}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        counter += 1
    
    # 5. Генерация QR-кода
    try:
        print("\n⏳ Генерация...")
        
        # Создаем QR-код
        qr = qrcode.QRCode(
            version=version,
            error_correction={
                'L': qrcode.constants.ERROR_CORRECT_L,
                'M': qrcode.constants.ERROR_CORRECT_M,
                'Q': qrcode.constants.ERROR_CORRECT_Q,
                'H': qrcode.constants.ERROR_CORRECT_H
            }[ec],
            box_size=box,
            border=4
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Сохраняем
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)
        
        print(f"✅ QR-код сохранен: {filepath}")
        save_history(text, filename, True)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        save_history(text, "ОШИБКА", False)

# === ГЛАВНОЕ МЕНЮ ===

def main():
    print("\n" + "="*40)
    print("   ГЕНЕРАТОР QR-КОДОВ")
    print("="*40)
    
    while True:
        print("\n1. Создать QR-код")
        print("2. История")
        print("3. Выход")
        
        choice = input("Выберите (1-3): ").strip()
        
        if choice == "1":
            generate_qr()
        elif choice == "2":
            show_history()
        elif choice == "3":
            print("До свидания!")
            break
        else:
            print("❌ Неверный выбор!")

if __name__ == "__main__":
    main()