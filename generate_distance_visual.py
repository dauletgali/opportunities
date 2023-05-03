import pandas as pd 
import numpy as np 
from bokeh.io import output_file
from bokeh.plotting import figure, show
from bokeh.layouts import column, gridplot
from bokeh.models import CustomJS, Select, HoverTool, BoxAnnotation, ColumnDataSource, CDSView, CustomJSFilter, Range1d, Div



data = pd.read_pickle(r"C:\Users\Sana\OneDrive\Desht\Digital lab\entity database\opportunities_data.pkl")
source = ColumnDataSource(data)

print(source.data)

list_of_regions = [
('all', 'Все'), 
('1110', 'Акмолинская область,Кокшетау Г.А.'),
 ('1510', 'Актюбинская область,Актобе Г.А.'),
 ('1968', 'Алматинская область,Илийский район'),
 ('2310', 'Атырауская область,Атырау Г.А.'),
 ('6324', 'Восточно-Казахстанская область,Риддер Г.А.'),
 ('6310', 'Восточно-Казахстанская область,Усть-Каменогорск Г.А.'),
 ('6348', 'Восточно-Казахстанская область,район Алтай'),
 ('3110', 'Жамбылская область,Тараз Г.А.'),
 ('2710', 'Западно-Казахстанская область,Уральск Г.А.'),
 ('3510', 'Карагандинская область,Караганда Г.А.'),
 ('3524', 'Карагандинская область,Темиртау Г.А.'),
 ('3528', 'Карагандинская область,Шахтинск Г.А.'),
 ('3910', 'Костанайская область,Костанай Г.А.'),
 ('3924', 'Костанайская область,Рудный Г.А.'),
 ('4332', 'Кызылординская область,Аральский район'),
 ('4346', 'Кызылординская область,Кармакшинский район'),
 ('4710', 'Мангистауская область,Актау Г.А.'),
 ('5510', 'Павлодарская область,Павлодар Г.А.'),
 ('5522', 'Павлодарская область,Экибастуз Г.А.'),
 ('5910', 'Северо-Казахстанская область,Петропавловск Г.А.'),
 ('7512', 'г.Алматы,Алатауский район'),
 ('7511', 'г.Алматы,Алмалинский район'),
 ('7513', 'г.Алматы,Ауэзовский район'),
 ('7514', 'г.Алматы,Бостандыкский район'),
 ('7515', 'г.Алматы,Жетысуский район'),
 ('7517', 'г.Алматы,Медеуский район'),
 ('7518', 'г.Алматы,Наурызбайский район'),
 ('7519', 'г.Алматы,Турксибский район'),
 ('7111', 'г.Нур-Султан,район Алматы'),
 ('7114', 'г.Нур-Султан,район Байқоңыр'),
 ('7112', 'г.Нур-Султан,район Есиль'),
 ('7113', 'г.Нур-Султан,район Сарыарка'),
 ('7915', 'г.Шымкент,Енбекшинский район'),
 ('1010', 'область Абай,Семей Г.А.')]


select_region = Select(title='Регион', value='all', options=list_of_regions)

codes_region = """
console.log(region.value)
const indices = [];

// iterate through rows of data source and see if each satisfies some constraint
for (let i = 0; i < source.get_length(); i++){
    console.log(source.data['kato4'][i])
    if (source.data['kato4'][i] == region.value || region.value == 'all'){
        indices.push(true);
    } else {
        indices.push(false);
    }
}
return indices;

"""

custom_filter = CustomJSFilter(args=dict(region = select_region) , code=codes_region)

select_region.js_on_change('value', CustomJS(args=dict(source=source) , code= """
source.change.emit()
"""))

data_view = CDSView(filter =custom_filter)


p = figure(title='Возможности', tools="pan,wheel_zoom,save,reset", 
           active_scroll='wheel_zoom' , x_range=Range1d(0.45, 0.755), y_range=Range1d(-0.1, 2.82) ,sizing_mode='stretch_both' , min_width=700, min_height=750)

HOVER_TOOLTIPS = [("Название отрасли", "@Oked_name") , ('RCA', '@rca{0.00}') , ('Дистанция' , '@distance') , ('Регион', '@kato_name'), ('HHI' , '@share_squared{0.00}')]
p.add_tools( HoverTool(tooltips=HOVER_TOOLTIPS , attachment='vertical'))


## Adding box annotations 
low_left = BoxAnnotation(right=0.6, top=1.145, fill_color='lime', fill_alpha=0.2)
low_right = BoxAnnotation(left=0.6, top=1.145, fill_color='red', fill_alpha=0.2)
top_left = BoxAnnotation(left=0.6, bottom=1.145, fill_color='orange', fill_alpha=0.2)
top_right = BoxAnnotation(right=0.6, bottom=1.145, fill_color='dodgerblue', fill_alpha=0.2)


p.add_layout(low_left)
p.add_layout(low_right)
p.add_layout(top_left)
p.add_layout(top_right)


p.circle(x='distance', y='rca_root', size=10,  fill_color='color', view=data_view, source=source)

p.xaxis.axis_label = "Дистанция"
p.yaxis.axis_label = r"$$RCA^{\frac{1}{3}}$$"
p.yaxis.axis_label_text_font_size = "15px"
p.xaxis.axis_label_text_font_size = "15px"
p.yaxis.axis_label_text_font_style = "bold"
p.xaxis.axis_label_text_font_style = "bold"

div = Div(text=""" <h3>ОСИ</h3> <br> <p> <b>Дистанция</b> – измерение вероятности специализации региона в индустрии, с учетом текущей корзины отраслей. Шкала от 0 до 1, причем чем ближе к 0, тем лучше <i>(меньше дистанция до новой индустрии)</i>. Дистанцию можно рассматривать, как меру риска входа в индустрию. Большое значение означает недостаток неких факторов, знаний, компетенций и ресурсов в регионе.</p><br>
<p><b>RCA</b> – индекс специализации или сравнительной представленности индустрии в регионе. Чем больше, тем лучше. На графике RCA взят в степень 1/3, для визуального удобства.</p>
<br> 
<h3>КВАДРАНТЫ</h3>
<p><b>Зеленый – «Арбитраж».</b> Низкий RCA и низкая дистанция. Индустрия в регионе еще не освоена, но потенциал высок.</p> <br>
  
<p><b>Синий – «Логика».</b> Высокий RCA и низкая дистанция. Был высокий потенциал освоения, и он реализован – индустрия хорошо представлена в регионе, высока конкуренция. Возможность кластерного развития.</p> <br> 
 
<p><b>Оранжевый – «Случайность».</b> Высокий RCA и высокая дистанция. Индустрия была нелогична в регионе, но специализация появилась. Ситуация случается при крупных проектах или государственных организациях и компаниях.</p> <br>

<p><b>Красный – «Риски».</b> Низкий RCA и высокая дистанция. Индустрия не представлена в регионе и этому нет предпосылок.</p> <br>

<h3>ЦВЕТА</h3> 
<p><b>Зелёный - </b>Низкая концентрация</p><br>
<p><b>Жёлтый - </b>Средняя концентрация</p><br>
<p><b>Красный - </b>Высокая концентрация</p><br>

""",
width=270, height=5000)


layout = gridplot([[div, column([select_region, p])]])

show(layout)