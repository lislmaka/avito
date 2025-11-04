        rls = []

        # Есть ли рядом магазин
        distance = 500
        flag_magazin = False
        if flat.to_magazin and int(flat.to_magazin) <= distance:
            flag_magazin = True
        if flat.to_pyaterochka and int(flat.to_pyaterochka) <= distance:
            flag_magazin = True
        if flat.to_magnit and int(flat.to_magnit) <= distance:
            flag_magazin = True

        if flag_magazin:
            rls.append(1)
        else:
            rls.append(0)

        # Есть ли рядом аптека
        if flat.to_apteka and int(flat.to_apteka) <= distance:
            rls.append(1)
        else:
            rls.append(0)

        # Есть ли рядом какой-то пункт выдачи товаров
        flag_delivery = False
        if flat.to_ozon and int(flat.to_ozon) <= distance:
            flag_delivery = True
        if flat.to_wildberries and int(flat.to_wildberries) <= distance:
            flag_delivery = True
        if flat.to_yandex and int(flat.to_yandex) <= distance:
            flag_delivery = True

        if flag_delivery:
            rls.append(1)
        else:
            rls.append(0)