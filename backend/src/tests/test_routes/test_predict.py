def test_predict(client):
    data = {"lot_no":"test"}
    response = client.post('/upload_file',json=data)
    assert response.status_code == 200
    # assert response.json()[]
    # res = ShowNG(plate_no=file.filename.split(".")[0],
    #             ng_chips=NG,
    #             img_shape=img_shape,
    #             no_of_chips=no_of_chips,
    #             no_of_batches=no_of_batches,
    #             ng_count=ng_count,
    #             directory=save_dir,
    #             chip_type=chip_type)