use QLDNUD
CREATE TABLE FolderTree (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ParentID INT NULL,
    Name NVARCHAR(255) NOT NULL,
    Level INT NOT NULL,   -- Cấp độ: 1 → 11
    Description NVARCHAR(MAX) NULL
);

CREATE TABLE Files (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    FolderID INT NOT NULL,
    FileName NVARCHAR(255) NOT NULL,        -- tên gốc
    StoredName NVARCHAR(255) NOT NULL,      -- tên UUID lưu trên server
    FileType NVARCHAR(50) NULL,             -- pdf, docx, xlsx, jpg...
    FileSize BIGINT NULL,                   -- dung lượng
    UploadedAt DATETIME DEFAULT GETDATE(),
    Description NVARCHAR(MAX) NULL,

    CONSTRAINT FK_Files_Folder FOREIGN KEY (FolderID)
        REFERENCES FolderTree(ID)
        ON DELETE CASCADE
);

ALTER TABLE FolderTree
ADD CONSTRAINT FK_FolderTree_Parent
FOREIGN KEY (ParentID) REFERENCES FolderTree(ID)
ON DELETE NO ACTION;

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (NULL, N'Quản lý', 1);
DECLARE @QL INT = SCOPE_IDENTITY();

-------------------------------------------------------------------------------------------------------------------------
DECLARE @NangLuong INT, @NM1 INT, @NM2 INT;

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (1, N'Năng lượng', 2);
SET @NangLuong = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (1, N'Nhà máy 1', 2);
SET @NM1 = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (1, N'Nhà máy 2', 2);
SET @NM2 = SCOPE_IDENTITY();
-----------------------------------------------------------------------------------------------
DECLARE @VuViec INT, @ThongKe INT, @VBQP INT, @BaoCaoTinhHinh INT;

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Vụ việc', 3);
SET @VuViec = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Thống kê', 3);
SET @ThongKe = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Văn bản quy phạm', 3);
SET @VBQP = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Báo cáo tình hình', 3);
SET @BaoCaoTinhHinh = SCOPE_IDENTITY();
-----------------------------------------------------------------------------------------
DECLARE @HanhChinh INT, @HinhSu INT;

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@VuViec, N'Hành chính', 4);
SET @HanhChinh = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@VuViec, N'Hình sự', 4);
SET @HinhSu = SCOPE_IDENTITY();
----------------------------------------------------------------------------------------
USE QLDNUD;
GO
--delete from FolderTree
--DBCC CHECKIDENT ('FolderTree', RESEED, 0)
-- ===== Declare all variables =====
DECLARE @QL INT, @NangLuong INT, @NM1 INT, @NM2 INT, @NMn INT;
DECLARE @VuViec INT, @ThongKe INT, @VBQP INT, @BC INT;
DECLARE @Than INT, @ThongKeThan INT, @DSDN INT;
DECLARE @QuanA INT, @QuanB INT;
DECLARE @Ph1 INT, @Ph2 INT;
DECLARE @Dn1 INT, @Dn2 INT;
DECLARE @Vt INT;

-- ===== Cấp 1 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (NULL, N'Quản lý', 1);
SET @QL = SCOPE_IDENTITY();

-- ===== Cấp 2 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@QL, N'Năng lượng', 2);
SET @NangLuong = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@QL, N'Nhà máy 1', 2);
SET @NM1 = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@QL, N'Nhà máy 2', 2);
SET @NM2 = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@QL, N'Nhà máy n', 2);
SET @NMn = SCOPE_IDENTITY();

-- ===== Cấp 3 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Vụ việc', 3);
SET @VuViec = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Thống kê', 3);
SET @ThongKe = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Văn bản quy phạm', 3);
SET @VBQP = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@NangLuong, N'Báo cáo tình hình', 3);
SET @BC = SCOPE_IDENTITY();

-- ===== Cấp 4 từ Vụ việc =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@VuViec, N'Hành chính', 4);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@VuViec, N'Hình sự', 4);

-- ===== Cấp 4 từ Thống kê =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKe, N'XD', 4);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKe, N'Than', 4);
SET @Than = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKe, N'Khí', 4);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKe, N'Điện', 4);

-- ===== Cấp 5 từ Than =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Than, N'Vụ việc', 5);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Than, N'Văn bản', 5);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Than, N'Báo cáo tình hình', 5);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Than, N'Thống kê', 5);
SET @ThongKeThan = SCOPE_IDENTITY();

-- ===== Cấp 6 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKeThan, N'Báo cáo tình hình', 6);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKeThan, N'Danh sách bến cảng nội địa', 6);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@ThongKeThan, N'Danh sách doanh nghiệp', 6);
SET @DSDN = SCOPE_IDENTITY();

-- ===== Cấp 7 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@DSDN, N'Quận A', 7);
SET @QuanA = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@DSDN, N'Quận B', 7);
SET @QuanB = SCOPE_IDENTITY();

-- ===== Cấp 8 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@QuanA, N'Phường 1', 8);
SET @Ph1 = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@QuanA, N'Phường 2', 8);
SET @Ph2 = SCOPE_IDENTITY();

-- ===== Cấp 9 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Ph1, N'Doanh nghiệp 1', 9);
SET @Dn1 = SCOPE_IDENTITY();

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Ph1, N'Doanh nghiệp 2', 9);
SET @Dn2 = SCOPE_IDENTITY();

-- ===== Cấp 10 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Dn1, N'Kết quả kinh doanh', 10);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Dn1, N'Vụ việc liên quan', 10);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Dn1, N'Báo cáo tài chính', 10);

INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Dn1, N'Vị trí doanh nghiệp', 10);
SET @Vt = SCOPE_IDENTITY();

-- ===== Cấp 11 =====
INSERT INTO FolderTree (ParentID, Name, Level)
VALUES (@Vt, N'Thông tin doanh nghiệp', 11);
