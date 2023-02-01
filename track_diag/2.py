x = '大妈离职，收到你别出你的从内地市场v吧新农村的赛场上'
y = '到你别'
if y in x:
    print('xxxxx')


_popup._tooltip.setContent(`<i class= "fa fa-clock-o" style = "color: black" > < /i>
${new Date(tt.alt*1000).toISOString().slice(11,19)}
<i class="fa fa-map-marker" style="color: dodgerblue"></i > Lat:${tt.lat.toFixed(3)},Lon:${tt.lng.toFixed(3)}<hr>
${diags.map(v => {
return `<i class="fa fa-spin fa-bug" style="color: red"></i>${v.level}
<font color="orange">${v.name}( ${v.msg} )</font>\n
<i class="fa fa-calendar" style="color: black"></i>${v.st_time} ~ ${v.et_time}`
}).join('<hr>')}`);