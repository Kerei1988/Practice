import os
import pandas as pd


class PriceMachine():
    
    def __init__(self):
        self.data = []
    
    def load_prices(self, file_path=''):
        possible_names = ["товар", "название", "наименование", "продукт", "розница", "цена", "вес", "масса", "фасовка",
                          'Файл']
        files = [file for file in os.listdir(file_path) if "price" in file]
        for file in files:
            df = pd.read_csv(file, sep=',')
            file_name = os.path.basename(file)
            df['Файл'] = file_name
            df_ = df.loc[:, df.columns.intersection(possible_names)]
            for column in df_.columns:
                if column in ["товар", "название", "наименование", "продукт"]:
                    df_.rename(columns={str(column): 'Название'}, inplace=True)
                if column in ["розница", "цена"]:
                    df_.rename(columns={str(column): 'Цена'}, inplace=True)
                if column in ["вес", "масса", "фасовка"]:
                    df_.rename(columns={str(column): 'Фасовка, кг'}, inplace=True)
            self.data.append(df_)
        self.data = pd.concat(self.data, ignore_index=True)
        return self.data


    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for number, item in enumerate(self.data.values.tolist()):
            name, weight, price, file = item
            result += '<tr>'
            result += f'\n<th>{number + 1}</th>'
            result += f'<th>{name}</th>'
            result += f'<th>{weight}</th>'
            result += f'<th>{price}</th>'
            result += f'<th>{file}</th>'
            result += '</tr>'
        result += '\n</table></body>'
        result += '\n</html>'
        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(result)
        return "Данные выгружены в файл 'output.html'"

    def find_text(self, text):
        keyword = text.lower()
        self.data['Название'] = self.data.loc[:, "Название"].apply(lambda x: x.lower())
        filter_data = self.data[self.data['Название'].str.contains(keyword) == True]
        filter_data['Цена за кг'] = (filter_data['Цена'] / filter_data['Фасовка, кг']).apply(lambda x: f'{x:.2f}').astype(float)
        sorted_data = filter_data.sort_values('Цена за кг', ascending=True)
        sorted_data.index = range(1, len(sorted_data) + 1)
        return sorted_data


path = "D:\Практика"
pm = PriceMachine()
print(pm.load_prices(path))

while True:
    user_input = input("Введите фрагмент названия товара (или exit для завершения): ")
    if user_input.lower() == "exit":
        print("Работа завершена.")
        break
    else:
        result = pm.find_text(user_input)
        if not result.empty:
            print(result)
        else:
            print("Товар не найден.")
print('the end')
print(pm.export_to_html())
