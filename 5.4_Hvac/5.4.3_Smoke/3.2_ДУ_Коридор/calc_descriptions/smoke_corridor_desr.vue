<template>
    <div>
    <h1>Расчёт параметров пожара и удаления продуктов горения</h1>

    <h2>1. Расчёт удельного критического количества пожарной нагрузки</h2>
    <p>Формула для расчёта:</p>
    <p style="text-align: center;">
        <code>g<sub>0</sub> = (M ∑m<sub>i</sub>Q<sup>p</sup><sub>нi</sub>) / (F<sub>f</sub>Q<sup>p</sup><sub>нд</sub>)</code>
    </p>
    <ul>
        <li><code>g<sub>0</sub></code> — удельное критическое количество пожарной нагрузки, кг/м²;</li>
        <li><code>M</code> — масса пожарной нагрузки помещения, кг;</li>
        <li><code>m<sub>i</sub></code> — относительная массовая доля i-го материала в составе пожарной нагрузки;</li>
        <li><code>Q<sup>p</sup><sub>нi</sub></code> — теплота сгорания i-го материала, Дж/кг;</li>
        <li><code>F<sub>f</sub></code> — площадь пола помещения, м²;</li>
        <li><code>Q<sup>p</sup><sub>нд</sub></code> — теплота сгорания древесины, Дж/кг.</li>
    </ul>

    <h2>2. Сравнение удельной пожарной нагрузки с критическим значением</h2>
    <p>Сравнение величины приведённой удельной пожарной нагрузки помещения с её критическим значением:</p>
    <ul>
        <li>Если <code>g<sub>k</sub> > g<sub>kкр</sub></code> — в помещении будет пожар, регулируемый вентиляцией (ПРВ);</li>
        <li>Если <code>g<sub>k</sub> < g<sub>kкр</sub></code> — в помещении будет пожар, регулируемый нагрузкой (ПРН).</li>
    </ul>

    <h2>3. Расчёт максимальной среднеобъёмной температуры</h2>
    <p>Для ПРВ:</p>
    <p style="text-align: center;">
        <code>T<sub>omax</sub> = T<sub>r</sub> + 940 exp(0.0047 × g<sub>o</sub> – 0.141)</code>
    </p>
    <p>Для ПРН:</p>
    <p style="text-align: center;">
        <code>T<sub>omax</sub> = T<sub>r</sub> + 224 g<sub>k</sub><sup>0.528</sup></code>
    </p>
    <ul>
        <li><code>T<sub>omax</sub></code> — максимальная среднеобъёмная температура в горящем помещении, К;</li>
        <li><code>T<sub>r</sub></code> — искомое значение температуры газов, поступающих из горящего помещения в коридор, К.</li>
    </ul>

    <h2>4. Расчёт искомой температуры газов</h2>
    <p style="text-align: center;">
        <code>T<sub>o</sub> = 0.8 × T<sub>omax</sub></code>
    </p>
    <ul>
        <li><code>T<sub>o</sub></code> — искомое значение температуры газов, поступающих из горящего помещения в коридор, К.</li>
    </ul>

    <h2>5. Ограничение по толщине дымового слоя</h2>
    <p style="text-align: center;">
        <code>0.5 ≤ h<sub>sm</sub>/H ≤ 0.6</code>
    </p>
    <ul>
        <li><code>h<sub>sm</sub></code> — предельная толщина дымового слоя, м;</li>
        <li><code>H</code> — высота коридора, м.</li>
    </ul>

    <h2>6. Расчёт массового расхода удаляемых продуктов горения</h2>
    <p style="text-align: center;">
        <code>G<sub>sm</sub> = k<sub>sm</sub>A<sub>d</sub>H<sub>d</sub><sup>0.5</sup></code>
    </p>
    <ul>
        <li><code>G<sub>sm</sub></code> — массовый расход удаляемых непосредственно из коридоров продуктов горения, кг/с;</li>
        <li><code>k<sub>sm</sub></code> — поправочный коэффициент на тип здания;</li>
        <li><code>A<sub>d</sub></code> — площадь двери при выходе из коридора по путям эвакуации, м²;</li>
        <li><code>H<sub>d</sub></code> — высота двери коридора, м.</li>
    </ul>
    <h2>7. Расчёт средней температуры дымового слоя</h2>
    <p>Формула для расчёта:</p>
    <p style="text-align: center;">
    <code>T<sub>sm</sub> = T<sub>r</sub> + 
    1.22(T<sub>o</sub> - T<sub>r</sub>)(2h<sub>sm</sub> + A<sub>c</sub>/l<sub>c</sub>) / l<sub>c</sub> × 
    (1 - exp(-0.58l<sub>c</sub> / (2h<sub>sm</sub> + A<sub>c</sub>/l<sub>c</sub>)))</code>
    </p>
    <ul>
    <li><code>T<sub>sm</sub></code> — средняя температура дымового слоя, К;</li>
    <li><code>T<sub>r</sub></code> — температура воздуха в коридоре, К;</li>
    <li><code>T<sub>o</sub></code> — искомое значение температуры газов, поступающих из горящего помещения в коридор, К;</li>
    <li><code>h<sub>sm</sub></code> — предельная толщина дымового слоя, м;</li>
    <li><code>A<sub>c</sub></code> — площадь коридора, м²;</li>
    <li><code>l<sub>c</sub></code> — длина коридора, м.</li>
    </ul>

    <h2>8. Расчёт объёмного расхода удаляемых продуктов горения</h2>
    <p style="text-align: center;">
    <code>L<sub>sm</sub> = 3600 × G<sub>sm</sub> / ρ<sub>sm</sub></code>
    </p>
    <ul>
    <li><code>L<sub>sm</sub></code> — объёмный расход удаляемых непосредственно из коридоров продуктов горения, м³/ч;</li>
    <li><code>G<sub>sm</sub></code> — массовый расход удаляемых непосредственно из коридоров продуктов горения, кг/с;</li>
    <li><code>ρ<sub>sm</sub></code> — средняя плотность газа в дымовом слое, кг/м³.</li>
    </ul>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.no-spin::-webkit-outer-spin-button,
.no-spin::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.no-spin[type="number"] { -moz-appearance: textfield; }
</style>