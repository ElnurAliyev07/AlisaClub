from django import template
from datetime import datetime

register = template.Library()

AY_ADLARI = {
    1: 'Yanvar',
    2: 'Fevral',
    3: 'Mart',
    4: 'Aprel',
    5: 'May',
    6: 'İyun',
    7: 'İyul',
    8: 'Avqust',
    9: 'Sentyabr',
    10: 'Oktyabr',
    11: 'Noyabr',
    12: 'Dekabr',
}

AY_ADLARI_QISA = {
    1: 'Yan',
    2: 'Fev',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'İyn',
    7: 'İyl',
    8: 'Avq',
    9: 'Sen',
    10: 'Okt',
    11: 'Noy',
    12: 'Dek',
}


@register.filter
def az_tarix(tarix, format='uzun'):
    """Azərbaycan dilində tarix formatı"""
    if not tarix:
        return ''
    
    if isinstance(tarix, str):
        tarix = datetime.strptime(tarix, '%Y-%m-%d')
    
    gun = tarix.day
    ay = AY_ADLARI[tarix.month] if format == 'uzun' else AY_ADLARI_QISA[tarix.month]
    il = tarix.year
    
    return f"{gun} {ay}, {il}"
