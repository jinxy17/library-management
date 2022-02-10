'''
Test suite for Resources
'''
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class TestResourcesEndpoint(TestCase):
    '''
    TestCase for /Resources
    '''

    def test_root(self):
        '''Test root'''
        response = self.client.get('/Resources/')

        self.assertEqual(response.status_code, 200)

    def test_lib(self):
        '''Test lib'''
        response = self.client.get('/Resources/yifu/')
        self.assertEqual(response.status_code, 200)
    
    def test_floor(self):
        '''Test floor'''
        response = self.client.get('/Resources/yifu/2/')
        self.assertEqual(response.status_code, 200)


    def test_submit(self):
        '''Test submit'''
        img = SimpleUploadedFile("img.jpg", b"file_content", content_type="multipart/form-data")
        response = self.client.post("/Resources/submit/addpic/yifu/2/intloan", {'data': img})
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/Resources/submit/delpic/yifu/2/intloan/img.jpg")
        self.assertEqual(response.status_code, 200)

        coods = {
            "x": 310,
            "y": 250
        }
        response = self.client.post("/Resources/submit/updcod/yifu/2/intloan", data=coods)
        self.assertEqual(response.status_code, 200)